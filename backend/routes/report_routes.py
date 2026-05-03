from flask import Blueprint, jsonify
from utils.sample_data import get_report

report_bp = Blueprint('report', __name__)


@report_bp.route('/api/report/<case_id>', methods=['GET'])
def get_case_report(case_id):
    report = get_report()
    if not report or report.get('case_id') != case_id:
        return jsonify({"message": "Report not found"}), 404
    return jsonify(report)


@report_bp.route('/api/report/create', methods=['GET'])
def generate_report():
    return jsonify(get_report())