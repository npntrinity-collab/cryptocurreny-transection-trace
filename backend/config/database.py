from pymongo import MongoClient

# 🔐 Replace with your MongoDB Atlas connection string
MONGO_URI = "mongodb://localhost:27017/"  
# (Later you can replace with Atlas URI)

client = MongoClient(MONGO_URI)

# Database name
db = client["crypto_trace_db"]

# Collections (tables)
cases_collection = db["cases"]
transactions_collection = db["transactions"]
wallets_collection = db["wallets"]
reports_collection = db["reports"]