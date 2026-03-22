id="svc1"
def fetch_transactions(wallet_address):
    """
    Simulated blockchain fetch (replace with real API later)
    """

    return [
        {"from": "Wallet A", "to": "Wallet B", "amount": 5},
        {"from": "Wallet B", "to": "Mixer", "amount": 10},
        {"from": "Mixer", "to": "Darknet", "amount": 8},
        {"from": "Darknet", "to": "Exchange", "amount": 7}
    ]