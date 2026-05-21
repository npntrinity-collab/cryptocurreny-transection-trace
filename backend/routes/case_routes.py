from datetime import datetime

from flask import Blueprint, request, jsonify, current_app
from config.database import cases_collection
from utils.helpers import generate_case_id
from utils.sample_data import get_cases as get_sample_cases

case_bp = Blueprint('case', __name__)


def _serialize_case(document):
    if not document:
        return None
    document.pop('_id', None)
    return document


# ✅ CREATE CASE
@case_bp.route('/api/cases', methods=['POST'])
def create_case():
    data = request.json or {}
    case = {
        "case_id": generate_case_id(),
        "title": data.get("title", "Untitled Case"),
        "wallet": data.get("wallet", ""),
        "status": data.get("status", "ACTIVE"),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    try:
        cases_collection.insert_one(case)
    except Exception as e:
        current_app.logger.warning('Create case DB insert failed, returning generated case only: %s', e)
    return jsonify(case)


# ✅ GET ALL CASES
@case_bp.route('/api/cases', methods=['GET'])
def get_cases():
    try:
        cases = list(cases_collection.find({}, {"_id": 0}).sort("created_at", -1))
    except Exception as e:
        current_app.logger.warning('Cases DB access failed, falling back to sample data: %s', e)
        return jsonify(get_sample_cases())

    if not cases:
        return jsonify(get_sample_cases())
    return jsonify(cases)


# ✅ DELETE CASE
@case_bp.route('/api/cases/<case_id>', methods=['DELETE'])
def delete_case(case_id):
    try:
        result = cases_collection.delete_one({"case_id": case_id})
    except Exception as e:
        current_app.logger.warning('Delete case DB delete failed: %s', e)
        return jsonify({"message": "Unable to delete case"}), 503
    if result.deleted_count == 0:
        return jsonify({"message": "Case not found"}), 404
    return jsonify({"message": "Deleted"})


# ✅ UPDATE CASE
@case_bp.route('/api/cases/<case_id>', methods=['PUT'])
def update_case(case_id):
    data = request.json or {}
    updated = {}
    if 'title' in data:
        updated['title'] = data['title']
    if 'wallet' in data:
        updated['wallet'] = data['wallet']
    if 'status' in data:
        updated['status'] = data['status']

    if not updated:
        return jsonify({"message": "No fields to update"}), 400

    try:
        result = cases_collection.find_one_and_update(
            {"case_id": case_id},
            {"$set": updated},
            return_document=True,
            projection={"_id": 0}
        )
    except Exception as e:
        current_app.logger.warning('Update case DB access failed: %s', e)
        return jsonify({
            "message": "Unable to update case",
            "error": str(e)
        }), 503

    if not result:
        return jsonify({"message": "Case not found"}), 404

    return jsonify(result)
