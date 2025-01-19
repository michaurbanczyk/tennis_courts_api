from contextlib import asynccontextmanager
from urllib.parse import quote_plus

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.db_connection import db_client

username = quote_plus("db_admin")
password = quote_plus("db_admin")
cluster = "cluster0.k2trl.mongodb.net"

uri = "mongodb+srv://" + username + ":" + password + "@" + cluster


# define a lifespan method for fastapi
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the database connection
    await startup_db_client(app)
    yield
    # Close the database connection
    await shutdown_db_client(app)


# method for start the MongoDb Connection
async def startup_db_client(app):
    app.mongodb_client = AsyncIOMotorClient(uri)
    app.mongodb = app.mongodb_client.get_database("tennis")
    db_client.db_client = app.mongodb
    print("MongoDB connected.")


# method to close the database connection
async def shutdown_db_client(app):
    app.mongodb_client.close()
    print("Database disconnected.")


def get_database(app: FastAPI) -> AsyncIOMotorClient:
    return app.mongodb


connected_clients = []
