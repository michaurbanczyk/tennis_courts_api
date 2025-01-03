import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.clubs import clubs_router
from app.routes.courts import courts_router
from app.routes.courts_data_status import courts_data_status
from app.routes.run_lambda import run_lambda_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(courts_router)
app.include_router(clubs_router)
app.include_router(run_lambda_router)
app.include_router(courts_data_status)

if __name__ == "__main__":
    uvicorn.run(app)
