import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.available_courts import available_courts_router
from app.routes.courts import courts_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(courts_router)
app.include_router(available_courts_router)

if __name__ == "__main__":
    uvicorn.run(app)
