id="svc3"
def detect_patterns(transactions):

    patterns = []

    for tx in transactions:

        if tx["to"].lower() == "mixer":
            patterns.append("Mixer Usage Detected")

        if tx["to"].lower() == "darknet":
            patterns.append("Darknet Market Transfer")

        if tx["amount"] >= 10:
            patterns.append("Large Transaction")

    return list(set(patterns))  # remove duplicates