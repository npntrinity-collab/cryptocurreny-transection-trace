from config.database import transactions_collection


def add_transaction(from_wallet, to_wallet, amount):
    transaction = {
        "from": from_wallet,
        "to": to_wallet,
        "amount": amount
    }
    transactions_collection.insert_one(transaction)
    return transaction


def get_transactions_by_wallet(wallet):
    return list(transactions_collection.find({
        "$or": [
            {"from": wallet},
            {"to": wallet}
        ]
    }))