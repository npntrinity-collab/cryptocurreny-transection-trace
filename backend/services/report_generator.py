id="svc6"
def generate_report(case_id, risk_data, exit_point):

    summary = f"""
    Case {case_id} Analysis:

    Risk Score: {risk_data['score']}
    Risk Level: {risk_data['level']}

    Flags:
    {', '.join(risk_data['flags'])}

    Exit Point:
    {exit_point}
    """

    return {
        "case_id": case_id,
        "summary": summary,
        "risk": risk_data
    }