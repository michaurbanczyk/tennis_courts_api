import pymongo
import uvicorn
from fastapi import FastAPI

from app.db.config import uri
from app.routes.courts import courts_router

app = FastAPI()

app.include_router(courts_router)

if __name__ == "__main__":
    client = pymongo.MongoClient(uri)
    uvicorn.run(app)
