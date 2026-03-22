from config.database import reports_collection
from datetime import datetime


def create_report(case_id, summary, risk_score):
    report = {
        "case_id": case_id,
        "summary": summary,
        "risk_score": risk_score,
        "generated_at": datetime.utcnow()
    }
    reports_collection.insert_one(report)
    return report


def get_report(case_id):
    return reports_collection.find_one({"case_id": case_id})