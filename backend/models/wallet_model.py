from config.database import wallets_collection


def add_wallet(address, wallet_type="normal"):
    wallet = {
        "address": address,
        "type": wallet_type
    }
    wallets_collection.insert_one(wallet)
    return wallet


def get_wallet(address):
    return wallets_collection.find_one({"address": address})