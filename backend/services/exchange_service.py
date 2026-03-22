id="svc5"
def identify_exit_point(transactions):

    for tx in transactions:
        if tx["to"].lower() == "exchange":
            return "Funds reached Exchange (Possible KYC)"

    return "No clear exit point" 