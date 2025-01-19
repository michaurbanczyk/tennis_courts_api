from contextlib import asynccontextmanager
from urllib.parse import quote_plus

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

username = quote_plus("db_admin")
password = quote_plus("db_admin")
cluster = "cluster0.k2trl.mongodb.net"

uri = "mongodb+srv://" + username + ":" + password + "@" + cluster

client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize MongoDB client
    global client
    client = AsyncIOMotorClient(uri)
    app.state.mongodb = client["tennis"]
    print("MongoDB connected")

    # Yield control to the app
    yield

    # Shutdown: Close MongoDB client
    client.close()
    print("MongoDB connection closed")


connected_clients = []
