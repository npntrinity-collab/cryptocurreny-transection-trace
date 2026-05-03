from flask import Blueprint, jsonify, request
from utils.sample_data import get_section

trace_bp = Blueprint('trace', __name__)


@trace_bp.route('/api/trace', methods=['GET'])
def trace():
    trace_data = get_section('trace', {})
    input_wallet = request.args.get('wallet') or trace_data.get('case', {}).get('input', 'Unknown Wallet')
    response = trace_data.copy()
    response['case'] = response.get('case', {}).copy()
    response['case']['input'] = input_wallet
    return jsonify(response)
