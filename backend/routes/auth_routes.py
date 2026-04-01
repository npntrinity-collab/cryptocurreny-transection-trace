from flask import Blueprint, request, jsonify
from config.database import db

auth_bp = Blueprint('auth', __name__)

users = db["users"]


@auth_bp.route('/api/signup', methods=['POST'])
def signup():

    data = request.json

    user = {
        "email": data["email"],
        "password": data["password"]
    }

    users.insert_one(user)

    return jsonify({"success": True})


@auth_bp.route('/api/login', methods=['POST'])
def login():

    data = request.json

    user = users.find_one({
        "email": data["email"],
        "password": data["password"]
    })

    if user:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})