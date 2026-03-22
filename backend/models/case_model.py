from config.database import cases_collection
from datetime import datetime


def create_case(case_id, input_wallet):
    case = {
        "case_id": case_id,
        "input_wallet": input_wallet,
        "status": "ACTIVE",
        "risk_score": 0,
        "created_at": datetime.utcnow()
    }
    cases_collection.insert_one(case)
    return case


def get_case(case_id):
    return cases_collection.find_one({"case_id": case_id})


def update_case_status(case_id, status):
    cases_collection.update_one(
        {"case_id": case_id},
        {"$set": {"status": status}}
    )