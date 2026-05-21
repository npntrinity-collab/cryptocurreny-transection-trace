from flask import Blueprint, jsonify, current_app
from config.database import reports_collection
from utils.sample_data import get_report

report_bp = Blueprint('report', __name__)


@report_bp.route('/api/report/<case_id>', methods=['GET'])
def get_case_report(case_id):
    report = None
    try:
        report = reports_collection.find_one({"case_id": case_id}, {"_id": 0})
    except Exception as e:
        current_app.logger.warning('Report DB access failed, falling back to sample data: %s', e)

    if report:
        return jsonify(report)

    sample_report = get_report()
    if sample_report and sample_report.get('case_id') == case_id:
        return jsonify(sample_report)

    return jsonify({"message": "Report not found"}), 404


@report_bp.route('/api/report/create', methods=['GET'])
def generate_report():
    # In a production app this would generate and save a report. For now, return sample data.
    return jsonify(get_report())