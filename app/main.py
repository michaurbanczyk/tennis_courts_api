import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.config import websocket_manager
from app.db.config import connected_clients
from app.routes.clubs import clubs_router
from app.routes.courts import courts_router
from app.routes.courts_data_status import courts_data_status
from app.routes.matches import matches_router
from app.routes.run_lambda import run_lambda_router
from app.routes.tournaments import tournaments_router

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
app.include_router(tournaments_router)
app.include_router(matches_router)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections."""
    await websocket.accept()
    websocket_manager.active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except Exception:
        websocket_manager.active_connections.remove(websocket)


if __name__ == "__main__":
    uvicorn.run(app)
