import os
import json
from datetime import datetime
import certifi
from pymongo import MongoClient, errors
from dotenv import load_dotenv


# Load `.env` from backend config
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))


def get_mongo_client():
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise RuntimeError("MONGO_URI environment variable is not set in backend/config/.env")
    return MongoClient(uri, tls=True, tlsCAFile=certifi.where())


def parse_iso_datetime(s):
    if not s:
        return None
    # Accept strings like 2026-05-16T08:30:00Z or with timezone
    try:
        if s.endswith('Z'):
            return datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
        return datetime.fromisoformat(s)
    except Exception:
        # Try common fallback
        try:
            return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        except Exception:
            return None


def import_cases_from_sample(db_name='crypto_trace_db', collection_name='cases', limit=0):
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sample_path = os.path.abspath(os.path.join(base, '..', 'database', 'sample_data.json'))

    with open(sample_path, 'r', encoding='utf-8') as fh:
        sample = json.load(fh)

    traces = sample.get('traces', {}) or {}

    docs = []
    for wallet, payload in traces.items():
        case = payload.get('case', {})
        doc = {
            'case_id': case.get('id') or f"CASE-{wallet[:6].upper()}",
            'title': f"Investigation {case.get('id', '')}",
            'wallet': case.get('input', wallet),
            'status': case.get('status', 'ACTIVE'),
            'assigned_investigator': case.get('assigned_investigator', ''),
            'priority': case.get('priority', ''),
            'created_at': parse_iso_datetime(case.get('created_at'))
        }
        docs.append(doc)
        if limit and len(docs) >= limit:
            break

    # If we don't have enough cases but dashboard expects 60, generate extras
    desired = 60
    if limit:
        desired = limit
    if len(docs) < desired:
        # generate synthetic cases based on existing ones
        idx = 1
        while len(docs) < desired:
            docs.append({
                'case_id': f'CASE-GEN-{idx:03d}',
                'title': f'Generated Case {idx}',
                'wallet': f'wallet_gen_{idx}',
                'status': 'ACTIVE',
                'assigned_investigator': 'AutoGen',
                'priority': 'LOW',
                'created_at': datetime.utcnow()
            })
            idx += 1

    client = None
    try:
        client = get_mongo_client()
        db = client[db_name]
        coll = db[collection_name]

        # Insert documents but avoid duplicates by case_id
        for doc in docs:
            try:
                coll.update_one({'case_id': doc['case_id']}, {'$set': doc}, upsert=True)
            except Exception as e:
                print('Failed to upsert', doc.get('case_id'), e)

        print(f'Imported/updated {len(docs)} case documents into {db_name}.{collection_name}')

    except errors.PyMongoError as e:
        print('PyMongo error during import:', e)
    finally:
        if client:
            client.close()


if __name__ == '__main__':
    import_cases_from_sample()
