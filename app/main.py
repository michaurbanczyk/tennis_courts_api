import asyncio

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.db.config import connected_clients
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
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
            print("ping")  # Keep connection alive
            await asyncio.sleep(30)
    except Exception:
        connected_clients.remove(websocket)


if __name__ == "__main__":
    uvicorn.run(app)
