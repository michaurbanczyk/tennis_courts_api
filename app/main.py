import asyncio

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.config import websocket_manager
from app.routes.matches import matches_router
from app.routes.tournaments import tournaments_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tournaments_router)
app.include_router(matches_router)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections."""
    await websocket.accept()
    websocket_manager.active_connections.append(websocket)
    heartbeat_task = asyncio.create_task(websocket_manager.send_heartbeat(websocket))
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.active_connections.remove(websocket)
    finally:
        heartbeat_task.cancel()


if __name__ == "__main__":
    uvicorn.run(app)
