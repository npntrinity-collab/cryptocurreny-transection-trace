from flask import Blueprint, jsonify, current_app
from config.database import dashboard_collection
from pymongo.errors import PyMongoError
from utils.sample_data import get_section

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard', methods=['GET'])
def dashboard():
    dashboard_data = None
    try:
        dashboard_data = dashboard_collection.find_one({}, {"_id": 0})
    except PyMongoError as e:
        current_app.logger.warning('Dashboard DB access failed, falling back to sample data: %s', e)
    if dashboard_data:
        return jsonify(dashboard_data)
    return jsonify(get_section('dashboard', {}))