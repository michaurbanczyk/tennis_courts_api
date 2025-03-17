import os
from urllib.parse import quote_plus

from motor.motor_asyncio import AsyncIOMotorClient

username = quote_plus(os.environ.get("DB_USERNAME"))
password = quote_plus(os.environ.get("DB_PASSWORD"))
cluster = os.environ.get("MONGO_DB_CLUSTER")

uri = "mongodb+srv://" + username + ":" + password + "@" + cluster
client = AsyncIOMotorClient(uri)

IS_PROD = os.environ.get("IS_PROD", False)

if IS_PROD:
    db = client["tennis"]
else:
    db = client["dev"]["tennis"]
