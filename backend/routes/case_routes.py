from flask import Blueprint, request, jsonify
from utils.helpers import generate_case_id
from utils.sample_data import get_cases

case_bp = Blueprint('case', __name__)

cases_data = get_cases().copy()

# ✅ CREATE CASE
@case_bp.route('/api/cases', methods=['POST'])
def create_case():

    data = request.json

    case = {
        "case_id": generate_case_id(),
        "title": data.get("title"),
        "wallet": data.get("wallet"),
        "status": "ACTIVE"
    }

    cases_data.append(case)

    return jsonify(case)


# ✅ GET ALL CASES
@case_bp.route('/api/cases', methods=['GET'])
def get_cases():
    return jsonify(cases_data)


# ✅ DELETE CASE
@case_bp.route('/api/cases/<case_id>', methods=['DELETE'])
def delete_case(case_id):
    global cases_data
    cases_data = [case for case in cases_data if case.get('case_id') != case_id]
    return jsonify({"message": "Deleted"})


# ✅ UPDATE CASE
@case_bp.route('/api/cases/<case_id>', methods=['PUT'])
def update_case(case_id):
    global cases_data
    data = request.json
    for case in cases_data:
        if case.get('case_id') == case_id:
            if 'title' in data:
                case['title'] = data['title']
            if 'wallet' in data:
                case['wallet'] = data['wallet']
            return jsonify(case)
    return jsonify({"message": "Case not found"}), 404