import uvicorn
from fastapi import FastAPI

from app.routes.available_courts import available_courts_router
from app.routes.courts import courts_router

app = FastAPI()

app.include_router(courts_router)
app.include_router(available_courts_router)

if __name__ == "__main__":
    uvicorn.run(app)
