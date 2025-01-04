import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.db.config import connected_clients, matches_collection
from app.routes.clubs import clubs_router
from app.routes.courts import courts_router
from app.routes.courts_data_status import courts_data_status
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


@app.post("/matches/")
async def create_match(match: dict):
    """Create a new tennis match."""
    result = await matches_collection.insert_one(match)
    match["_id"] = str(result.inserted_id)
    for client in connected_clients:
        await client.send_json({"event": "new_match", "data": match})
    return match


@app.get("/matches/")
async def get_matches():
    """Get all tennis matches."""
    matches = await matches_collection.find().to_list(100)
    for match in matches:
        match["_id"] = str(match["_id"])  # Convert ObjectId to string
    return matches


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections."""
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except Exception:
        connected_clients.remove(websocket)


if __name__ == "__main__":
    uvicorn.run(app)
