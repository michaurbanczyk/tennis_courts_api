from datetime import datetime, timezone
from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException

from app.db.config import db
from app.models.common import Response
from app.models.matches import MatchResponse
from app.models.tournaments import (
    TournamentCreate,
    TournamentResponse,
    TournamentStatus,
    TournamentUpdate,
)

tournaments_router = APIRouter(
    prefix="/tournaments",
    tags=["tournaments"],
)


@tournaments_router.get("/", response_model=List[TournamentResponse])
async def get_tournaments():
    tournaments = await db["tournaments"].find().to_list(100)
    if tournaments:
        return tournaments
    raise HTTPException(status_code=404, detail="No tournaments")


@tournaments_router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(tournament_id: str):
    tournament = await db["tournaments"].find_one({"_id": ObjectId(tournament_id)})
    if tournament:
        return tournament
    raise HTTPException(status_code=404, detail=f"Tournament with {tournament_id} not found")


@tournaments_router.post("/", status_code=201, response_model=Response)
async def create_tournament(tournament: TournamentCreate):
    tournament_model_dump = tournament.model_dump()
    current_time = datetime.now(timezone.utc).replace(tzinfo=None)
    tournament_to_create = {
        **tournament_model_dump,
        "status": TournamentStatus.PLANNED,
        "createdDate": current_time,
        "lastUpdateDate": current_time,
    }
    created_tournament = await db["tournaments"].insert_one(tournament_to_create)
    if not created_tournament:
        return HTTPException(status_code=500, detail="Tournament creation failed")

    return {"message": f"Tournament {tournament_model_dump['title']} created successfully"}


@tournaments_router.delete("/{tournament_id}", response_model=Response)
async def delete_tournament(tournament_id: str):
    result = await db["tournaments"].delete_one({"_id": ObjectId(tournament_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Tournament with id {tournament_id} not found")
    return {"message": f"Tournament with id {tournament_id} deleted successfully"}


@tournaments_router.patch("/{tournament_id}", response_model=TournamentResponse)
async def update_tournament(
    tournament_id: str,
    body: TournamentUpdate,
):
    body = body.model_dump(exclude_unset=True)
    tournament = await db["tournaments"].find_one({"_id": ObjectId(tournament_id)})
    if not tournament:
        raise HTTPException(status_code=404, detail=f"Tournament with id {tournament_id} not found")
    tournament_update = {**body, "lastUpdateDate": datetime.now(timezone.utc).replace(tzinfo=None)}
    result = await db["tournaments"].find_one_and_update(
        {"_id": ObjectId(tournament_id)}, {"$set": tournament_update}, return_document=True
    )
    return result


@tournaments_router.get("/{tournament_id}/matches", response_model=List[MatchResponse])
async def get_tournaments_matches(tournament_id: str):
    tournament_matches = await db["matches"].find({"tournamentId": tournament_id}).to_list(1000)
    if not tournament_matches:
        return []
    return tournament_matches
