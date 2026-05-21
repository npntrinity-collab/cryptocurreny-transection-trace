from flask import Blueprint, request, jsonify, current_app
from config.database import auth_collection
from pymongo.errors import PyMongoError
from utils.sample_data import get_auth

auth_bp = Blueprint('auth', __name__)


def _get_auth_user(email):
    try:
        return auth_collection.find_one({"email": email}, {"_id": 0})
    except PyMongoError as e:
        current_app.logger.warning('Auth DB access failed, falling back to sample auth: %s', e)
        return None


@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.json or {}
    user = {
        "email": data.get('email'),
        "password": data.get('password'),
        "role": "analyst"
    }
    try:
        auth_collection.insert_one(user)
    except PyMongoError as e:
        current_app.logger.warning('Auth signup DB insert failed: %s', e)
    return jsonify({"success": True, "user": {"email": user['email'], "role": user['role']}})


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    user = _get_auth_user(data.get('email'))
    if user and user.get('password') == data.get('password'):
        return jsonify({"success": True})

    sample_auth = get_auth()
    for sample_user in sample_auth.get('users', []):
        if sample_user.get('email') == data.get('email') and sample_user.get('password') == data.get('password'):
            return jsonify({"success": True})

    return jsonify({"success": False})