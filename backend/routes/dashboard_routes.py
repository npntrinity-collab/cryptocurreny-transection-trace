from flask import Blueprint, jsonify
from utils.sample_data import get_section

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard', methods=['GET'])
def dashboard():
    return jsonify(get_section('dashboard', {}))