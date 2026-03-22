from utils.constants import RISK_WEIGHTS
id="svc4"
def calculate_risk(patterns):

    score = 0

    for p in patterns:
        if "Mixer" in p:
            score += RISK_WEIGHTS["MIXER"]
        elif "Darknet" in p:
            score += 30
        elif "Large" in p:
            score += 20

    level = "LOW"

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"

    return {
        "score": score,
        "level": level,
        "flags": patterns
    }