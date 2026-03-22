from flask import Blueprint, jsonify
from models.report_model import create_report, get_report

report_bp = Blueprint('report', __name__)


@report_bp.route('/api/report/<case_id>', methods=['GET'])
def get_case_report(case_id):

    report = get_report(case_id)

    if not report:
        return jsonify({"message": "Report not found"}), 404

    return jsonify(report)


@report_bp.route('/api/report/create', methods=['GET'])
def generate_report():

    case_id = "CASE-001"

    report = create_report(
        case_id=case_id,
        summary="Funds traced through mixer and darknet to exchange.",
        risk_score=89
    )

    return jsonify(report)