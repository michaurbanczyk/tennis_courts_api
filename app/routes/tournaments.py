from datetime import datetime, timezone
from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query

from app.db.config import db
from app.models.common import Response
from app.models.matches import MatchResponse
from app.models.tournaments import (
    TournamentCreate,
    TournamentPassword,
    TournamentResponse,
    TournamentStatus,
    TournamentUpdate,
)
from app.routes.users import get_current_user

tournaments_router = APIRouter(
    prefix="/tournaments",
    tags=["tournaments"],
)


@tournaments_router.get("/", response_model=List[TournamentResponse])
async def get_tournaments(
    created_by: Optional[str] = Query(None, alias="createdBy", description="Filter by created_by"),
    is_private: Optional[bool] = Query(None, alias="isPrivate", description="Filter by is_private"),
):
    query = {}
    if created_by:
        query["createdBy"] = ObjectId(created_by)
    if is_private is not None:
        query["isPrivate"] = is_private

    tournaments = await db["tournaments"].find(query).to_list(100)
    if tournaments:
        return tournaments
    return []


@tournaments_router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(tournament_id: str):
    tournament = await db["tournaments"].find_one({"_id": ObjectId(tournament_id)})
    if tournament:
        return tournament
    raise HTTPException(status_code=404, detail=f"Tournament with {tournament_id} not found")


@tournaments_router.post("/", status_code=201, response_model=Response)
async def create_tournament(tournament: TournamentCreate, current_user: dict = Depends(get_current_user)):
    tournament_model_dump = tournament.model_dump()
    current_time = datetime.now(timezone.utc).replace(tzinfo=None)
    tournament_to_create = {
        **tournament_model_dump,
        "status": TournamentStatus.PLANNED,
        "createdDate": current_time,
        "lastUpdateDate": current_time,
        "createdBy": current_user["_id"],
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


@tournaments_router.post("/{tournament_id}/verify-password", response_model=Response)
async def verify_password(tournament_id: str, body: TournamentPassword):
    tournament = await db["tournaments"].find_one({"_id": ObjectId(tournament_id)})
    if tournament:
        body = body.model_dump()
        if tournament["password"] == body["password"]:
            return {"message": "Password correct"}
        else:
            raise HTTPException(status_code=401, detail="Password not correct")
    raise HTTPException(status_code=404, detail=f"Tournament with {tournament_id} not found")
