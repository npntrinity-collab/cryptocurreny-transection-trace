# cryptocurreny-transection-trace

This project is designed to trace cryptocurrency transactions and help analysts investigate suspicious transfers.

## MongoDB Setup

The backend connects to MongoDB using `backend/config/database.py`.

### Local MongoDB

If you have MongoDB installed locally, the app uses:

```python
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "crypto_trace_db"
```

### MongoDB Atlas

To use Atlas instead, update `backend/config/database.py` or set environment variables:

```bash
set MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
set MONGO_DB_NAME=crypto_trace_db
```

Then restart the backend server.

### Collections used

- `cases`
- `transactions`
- `wallets`
- `reports`
- `dashboard`
- `traces`
- `risk`
- `auth`
