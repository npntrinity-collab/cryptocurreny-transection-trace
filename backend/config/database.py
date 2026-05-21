import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv("backend/config/.env")

# Use environment variable first, otherwise fall back to local MongoDB.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "crypto_trace_db")

# Use short timeouts so a bad Mongo connection fails quickly and route fallbacks can execute.
client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000,
)

# Database name
db = client[MONGO_DB_NAME]

# Collections (tables)
cases_collection = db["cases"]
markets_collection = db["markets"]
transactions_collection = db["transactions"]
wallets_collection = db["wallets"]
reports_collection = db["reports"]
dashboard_collection = db["dashboard"]
traces_collection = db["traces"]
risk_collection = db["risk"]
auth_collection = db["auth"]