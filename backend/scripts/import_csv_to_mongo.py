import argparse
import csv
import json
import os
import re
import certifi
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient, errors

# Load project .env so MONGO_URI and related vars are available
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))

UNIT_MULTIPLIERS = {
    'thousand': 1e3,
    'million': 1e6,
    'billion': 1e9,
    'trillion': 1e12,
    'quadrillion': 1e15,
    'k': 1e3,
    'm': 1e6,
    'b': 1e9,
    't': 1e12,
}


def get_mongo_client():
    uri = os.getenv('MONGO_URI')
    if not uri:
        raise RuntimeError('MONGO_URI environment variable is not set')
    return MongoClient(
        uri,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
    )


def normalize_number(value):
    if value is None:
        return None
    text = str(value).strip().replace('"', '')
    if text == '' or text.lower() in {'n/a', 'na', '-', '∞', 'infinity'}:
        return None

    # Clean currency and separators
    cleaned = text.replace('$', '').replace(',', '').replace(' ', '')
    if cleaned == '':
        return None

    # Handle direct numeric values
    try:
        return float(cleaned)
    except ValueError:
        pass

    # Handle values with unit suffixes like 88.3B or 21Million
    match = re.match(r'^([+-]?[0-9]*\.?[0-9]+)\s*([A-Za-z]+)$', text.replace(',', '').strip())
    if match:
        num = float(match.group(1))
        unit = match.group(2).lower()
        return num * UNIT_MULTIPLIERS.get(unit, 1)

    # Fallback: remove non-numeric chars and try again
    cleaned = re.sub(r'[^0-9.+-]', '', text)
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_percent(value):
    if value is None:
        return None
    text = str(value).strip().replace('%', '').replace(' ', '')
    if text == '' or text.lower() in {'n/a', 'na', '-', '∞'}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def normalize_field_names(row):
    normalized = {}
    for key, val in row.items():
        if key is None:
            continue
        normalized[key.strip()] = val
    return normalized


def build_market_document(row):
    row = normalize_field_names(row)
    return {
        'rank': int(row.get('Rank')) if row.get('Rank') and row.get('Rank').strip().isdigit() else None,
        'name': row.get('Coin Name', '').strip(),
        'symbol': row.get('Symbol', '').strip(),
        'price_usd': normalize_number(row.get('Price')),
        'change_1h_pct': parse_percent(row.get('1h')),
        'change_24h_pct': parse_percent(row.get('24h')),
        'change_7d_pct': parse_percent(row.get('7d')),
        'change_30d_pct': parse_percent(row.get('30d')),
        'volume_24h_usd': normalize_number(row.get('24h Volume')),
        'circulating_supply': normalize_number(row.get('Circulating Supply')),
        'total_supply': normalize_number(row.get('Total Supply')),
        'market_cap_usd': normalize_number(row.get('Market Cap')),
        'source': 'crypto_markets.csv',
        'imported_at': datetime.utcnow().isoformat() + 'Z',
        'raw': row,
    }


def import_csv_to_collection(csv_path, db_name, collection_name='markets', batch_size=500):
    client = None
    try:
        client = get_mongo_client()
        db = client[db_name]
        coll = db[collection_name]

        inserted = 0
        skipped = 0
        with open(csv_path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames:
                reader.fieldnames = [h.strip() for h in reader.fieldnames]
            batch = []
            for row in reader:
                doc = build_market_document(row)
                if not doc['symbol'] or doc['name'] == '':
                    skipped += 1
                    continue
                batch.append(doc)
                if len(batch) >= batch_size:
                    coll.insert_many(batch)
                    inserted += len(batch)
                    batch = []
            if batch:
                coll.insert_many(batch)
                inserted += len(batch)

        print(f'Import complete: inserted {inserted} documents into {db_name}.{collection_name}, skipped {skipped} rows.')

    except errors.PyMongoError as e:
        print('PyMongo error during import:', e)
    except Exception as e:
        print('Error during import:', e)
    finally:
        if client:
            client.close()


def read_market_documents(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames:
            reader.fieldnames = [h.strip() for h in reader.fieldnames]
        for row in reader:
            yield build_market_document(row)


def export_csv_to_json(csv_path, output_path):
    docs = []
    skipped = 0
    for doc in read_market_documents(csv_path):
        if not doc['symbol'] or doc['name'] == '':
            skipped += 1
            continue
        docs.append(doc)
    with open(output_path, 'w', encoding='utf-8') as fh:
        json.dump(docs, fh, indent=2, ensure_ascii=False)
    print(f'Export complete: wrote {len(docs)} documents to {output_path}, skipped {skipped} rows.')


if __name__ == '__main__':
    import argparse
    # Default CSV path (repo-root relative)
    script_dir = os.path.dirname(__file__)
    default_csv = os.path.abspath(os.path.join(script_dir, '..', '..', 'database', 'crypto_markets.csv'))

    parser = argparse.ArgumentParser(description='Import or export crypto markets CSV data.')
    parser.add_argument('--csv', default=default_csv, help='Path to crypto_markets.csv')
    parser.add_argument('--db', default=os.getenv('MONGO_DB_NAME', 'crypto_trace_db'), help='MongoDB database name')
    parser.add_argument('--collection', default=os.getenv('MONGO_COLLECTION', 'markets'), help='MongoDB collection name')
    parser.add_argument('--batch-size', type=int, default=500, help='Batch size for inserts')
    parser.add_argument('--export-json', default=None, help='Path to write normalized JSON instead of importing')
    args = parser.parse_args()

    print('CSV path:', args.csv)
    print('Mongo DB:', args.db)
    if args.export_json:
        export_csv_to_json(args.csv, args.export_json)
    else:
        import_csv_to_collection(args.csv, args.db, args.collection, args.batch_size)
