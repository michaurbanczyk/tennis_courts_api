import logging

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

ws_router = APIRouter(
    prefix="/ws",
    tags=["ws"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logging.info(f"Active connections: {self.active_connections}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        message["_id"] = message["id"]
        del message["id"]
        for connection in self.active_connections:
            await connection.send_json(message)


connection_manager = ConnectionManager()


@ws_router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
