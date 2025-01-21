import asyncio
from typing import List

from fastapi import WebSocket, WebSocketDisconnect

MAX_CONNECTIONS = 1000
HEARTBEAT_INTERVAL = 1


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        if len(self.active_connections) >= MAX_CONNECTIONS:
            await websocket.close(code=1008)  # Connection limit exceeded
            return
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

    @staticmethod
    async def send_heartbeat(websocket: WebSocket):
        while True:
            try:
                await asyncio.sleep(HEARTBEAT_INTERVAL)
                await websocket.send_text("heartbeat")
            except WebSocketDisconnect:
                break
