from flask import Blueprint, request, jsonify
from utils.sample_data import get_auth

auth_bp = Blueprint('auth', __name__)

auth_data = get_auth().copy()


@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    auth_data.setdefault('users', []).append({
        "email": data.get('email'),
        "password": data.get('password')
    })
    return jsonify({"success": True, "user": {"email": data.get('email'), "role": "analyst"}})


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    users = auth_data.get('users', [])
    valid_user = any(user.get('email') == data.get('email') and user.get('password') == data.get('password') for user in users)
    return jsonify({"success": bool(valid_user)})