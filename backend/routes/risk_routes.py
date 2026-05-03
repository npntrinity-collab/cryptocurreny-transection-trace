from flask import Blueprint, jsonify
from utils.sample_data import get_section

risk_bp = Blueprint('risk', __name__)

@risk_bp.route('/api/risk', methods=['GET'])
def risk_data():
    return jsonify(get_section('riskPage', {}))
