id="help1"
import uuid
from datetime import datetime


# 🔹 Generate unique Case ID
def generate_case_id():
    return f"CASE-{uuid.uuid4().hex[:6].upper()}"


# 🔹 Format timestamp
def get_current_time():
    return datetime.utcnow()


# 🔹 Convert amount to BTC string
def format_btc(amount):
    return f"{amount} BTC"


# 🔹 Determine wallet type
def identify_wallet_type(name):

    name = name.lower()

    if "mixer" in name:
        return "mixer"
    elif "darknet" in name:
        return "darknet"
    elif "exchange" in name:
        return "exchange"
    else:
        return "normal"


# 🔹 Calculate total volume
def calculate_total_volume(transactions):

    total = 0

    for tx in transactions:
        total += tx["amount"]

    return total


# 🔹 Count unique wallets
def count_wallets(transactions):

    wallets = set()

    for tx in transactions:
        wallets.add(tx["from"])
        wallets.add(tx["to"])

    return len(wallets)


# 🔹 Count suspicious patterns
def count_suspicious(patterns):
    return len(patterns)