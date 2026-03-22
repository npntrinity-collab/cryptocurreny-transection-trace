from flask import Blueprint, jsonify, request
from models.case_model import create_case
from models.wallet_model import add_wallet
from models.transaction_model import add_transaction
from services.blockchain_service import fetch_transactions
from services.graph_builder import build_graph
from services.pattern_detector import detect_patterns
from services.risk_engine import calculate_risk
from services.exchange_service import identify_exit_point

trace_bp = Blueprint('trace', __name__)


@trace_bp.route('/api/trace', methods=['GET'])
def trace():

    # 🔹 Example input (later from request)
    input_wallet = "Wallet A"
    case_id = "CASE-001"

    # 🟢 Create Case
    create_case(case_id, input_wallet)

    # 🟢 Add Wallets
    add_wallet("Wallet A")
    add_wallet("Wallet B")
    add_wallet("Mixer", "mixer")
    add_wallet("Darknet", "darknet")
    add_wallet("Exchange", "exchange")

    # 🟢 Add Transactions
    add_transaction("Wallet A", "Wallet B", "5 BTC")
    add_transaction("Wallet B", "Mixer", "10 BTC")
    add_transaction("Mixer", "Darknet", "8 BTC")
    add_transaction("Darknet", "Exchange", "7 BTC")

    # 🧠 Fake Risk Logic (will upgrade later)
    risk_score = 89

    # 🧾 Response (Frontend format)
    return jsonify({

        "case": {
            "id": case_id,
            "input": input_wallet,
            "status": "ACTIVE"
        },

        "summary": {
            "totalVolume": "30 BTC",
            "wallets": 5,
            "transactions": 4,
            "suspicious": 3
        },

        "risk": {
            "score": risk_score,
            "level": "HIGH",
            "flags": [
                "Darknet Market Transfer",
                "Large Transaction",
                "Mixer Usage Detected"
            ]
        },

        "graph": {
            "nodes": [
                {"data": {"id": "A", "label": "Wallet A"}},
                {"data": {"id": "B", "label": "Wallet B"}},
                {"data": {"id": "MX", "label": "Mixer", "type": "mixer"}},
                {"data": {"id": "DN", "label": "Darknet", "type": "darknet"}},
                {"data": {"id": "EX", "label": "Exchange", "type": "exchange"}}
            ],
            "edges": [
                {"data": {"source": "A", "target": "B", "label": "5 BTC"}},
                {"data": {"source": "B", "target": "MX", "label": "10 BTC"}},
                {"data": {"source": "MX", "target": "DN", "label": "8 BTC"}},
                {"data": {"source": "DN", "target": "EX", "label": "7 BTC"}}
            ]
        },

        "timeline": [
            {"time": "10:25 AM", "text": "Wallet A → Wallet B"},
            {"time": "11:10 AM", "text": "Wallet B → Mixer"},
            {"time": "12:30 PM", "text": "Mixer → Darknet"},
            {"time": "01:15 PM", "text": "Darknet → Exchange"}
        ]

    })