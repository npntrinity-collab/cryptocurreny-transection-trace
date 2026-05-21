from flask import Blueprint, jsonify, current_app
from config.database import risk_collection
from pymongo.errors import PyMongoError
from utils.sample_data import get_section

risk_bp = Blueprint('risk', __name__)

@risk_bp.route('/api/risk', methods=['GET'])
def risk_data():
    risk_data = None
    try:
        risk_data = risk_collection.find_one({}, {"_id": 0})
    except PyMongoError as e:
        current_app.logger.warning('Risk DB access failed, falling back to sample data: %s', e)

    if risk_data:
        return jsonify(risk_data)
    return jsonify(get_section('riskPage', {}))
