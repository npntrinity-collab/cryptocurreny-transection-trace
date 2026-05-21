from flask import Blueprint, jsonify, request, current_app
import csv
import os

market_bp = Blueprint('market', __name__, url_prefix='/api')

# Load CSV once
DATA = []
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'crypto_markets.csv')

def parse_money(s):
    if not s:
        return 0.0
    try:
        # remove any non-digit, non-dot, non-minus
        cleaned = ''.join(ch for ch in s if (ch.isdigit() or ch in '.-'))
        return float(cleaned) if cleaned else 0.0
    except Exception:
        return 0.0

if os.path.exists(CSV_PATH):
    try:
        with open(CSV_PATH, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                market_cap_raw = row.get(' Market Cap ') or row.get('Market Cap') or row.get(' Market Cap') or ''
                market_cap = parse_money(market_cap_raw)
                price_raw = row.get(' Price ') or row.get('Price') or row.get(' Price') or ''
                price = parse_money(price_raw)
                DATA.append({
                    'rank': int(row.get('Rank') or 0),
                    'name': row.get('Coin Name') or row.get('Coin') or row.get('Coin Name '),
                    'symbol': row.get('Symbol') or '',
                    'price': price,
                    'market_cap': market_cap,
                    'raw': row
                })
            # sort by market cap desc
            DATA.sort(key=lambda x: x.get('market_cap', 0), reverse=True)
    except Exception as ex:
        current_app.logger if 'current_app' in globals() else None

@market_bp.route('/market')
def market_list():
    try:
        top = int(request.args.get('top', 10))
    except Exception:
        top = 10
    items = DATA[:top]
    # return compact fields
    out = [
        {'rank': i['rank'], 'name': i['name'], 'symbol': i['symbol'], 'price': i['price'], 'market_cap': i['market_cap']}
        for i in items
    ]
    return jsonify(out)
