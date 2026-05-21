import hashlib

from flask import Blueprint, jsonify, request, current_app
from config.database import traces_collection
from utils.sample_data import get_section

trace_bp = Blueprint('trace', __name__)


def build_dynamic_trace(wallet, default_trace):
    wallet_hash = hashlib.sha256(wallet.encode('utf-8')).hexdigest()
    seed = int(wallet_hash[:16], 16)

    node_types = [
        {"label": "Mixer", "type": "mixer"},
        {"label": "Cluster", "type": "cluster"},
        {"label": "Exchange", "type": "exchange"},
        {"label": "Sanctioned", "type": "sanctioned"}
    ]

    nodes = [{"data": {"id": "IN", "label": wallet, "type": "input"}}]
    for idx, entry in enumerate(node_types, start=1):
        nodes.append({"data": {"id": f"N{idx}", "label": entry["label"], "type": entry["type"]}})

    edges = []
    for idx in range(len(nodes) - 1):
        amount = 2 + ((seed >> (idx * 4)) % 18)
        edges.append({
            "data": {
                "source": nodes[idx]["data"]["id"],
                "target": nodes[idx + 1]["data"]["id"],
                "label": f"{amount} BTC"
            }
        })

    score = 60 + (seed % 41)
    flags = []
    if score >= 90:
        flags.append("High-Risk Counterparty")
    if seed % 2 == 0:
        flags.append("Mixer Usage Detected")
    if seed % 3 == 0:
        flags.append("Rapid Transfers")
    if seed % 5 == 0:
        flags.append("Darknet Links")
    if not flags:
        flags.append("Unusual Transfer Pattern")

    return {
        "case": {
            "id": f"CASE-{wallet_hash[:4].upper()}",
            "input": wallet,
            "status": "ACTIVE",
            "assigned_investigator": default_trace.get('case', {}).get('assigned_investigator', 'Crypto Analyst'),
            "priority": "MEDIUM",
            "created_at": default_trace.get('case', {}).get('created_at', '')
        },
        "summary": {
            "totalVolume": f"{sum((2 + ((seed >> (i * 4)) % 18) for i in range(len(nodes) - 1)))} BTC",
            "wallets": len(nodes),
            "transactions": len(edges),
            "suspicious": len(flags),
            "confirmed_clusters": 1,
            "possible_mixer_routes": 1,
            "average_hop_depth": round(len(edges) / 1.5, 1)
        },
        "risk": {
            "score": score,
            "level": "HIGH" if score >= 80 else "MEDIUM",
            "flags": flags,
            "exposure": {
                "mixer": f"{2 + (seed % 10)} BTC",
                "exchange": f"{3 + ((seed >> 6) % 8)} BTC"
            }
        },
        "graph": {
            "nodes": nodes,
            "edges": edges
        },
        "timeline": [
            {"time": "09:00 AM", "text": f"{wallet} → Mixer ( {2 + ((seed >> 2) % 18)} BTC )"},
            {"time": "09:25 AM", "text": f"Mixer → Cluster ( {3 + ((seed >> 4) % 12)} BTC )"},
            {"time": "09:45 AM", "text": f"Cluster → Exchange ( {4 + ((seed >> 6) % 10)} BTC )"},
            {"time": "10:05 AM", "text": f"Exchange → Sanctioned ( {5 + ((seed >> 8) % 8)} BTC )"}
        ]
    }


@trace_bp.route('/api/trace', methods=['GET'])
def trace():
    default_trace = get_section('trace', {})
    input_wallet = request.args.get('wallet') or default_trace.get('case', {}).get('input', 'Unknown Wallet')

    trace_doc = None
    try:
        trace_doc = traces_collection.find_one({"case.input": input_wallet}, {"_id": 0})
    except Exception as e:
        current_app.logger.warning('Trace DB access failed, using generated fallback data: %s', e)

    if trace_doc:
        response = trace_doc
    else:
        response = build_dynamic_trace(input_wallet, default_trace)

    response = response.copy()
    response['case'] = response.get('case', {}).copy()
    response['case']['input'] = input_wallet
    return jsonify(response)
