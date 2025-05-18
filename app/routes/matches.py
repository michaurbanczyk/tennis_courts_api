from datetime import datetime
from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException

from app.config import app_timezone
from app.db.config import db
from app.models.common import Response
from app.models.matches import (
    MatchCreate,
    MatchPassword,
    MatchResponse,
    MatchResultUpdate,
    MatchStatus,
    MatchUpdate,
)
from app.routes.websocket import connection_manager
from app.utils.get_players_passwords import get_players_passwords

matches_router = APIRouter(
    prefix="/matches",
    tags=["matches"],
)


@matches_router.get("", response_model=List[MatchResponse])
async def get_matches():
    matches = await db["matches"].find().to_list(100)
    if matches:
        return matches
    raise HTTPException(status_code=404, detail="No matches")


@matches_router.get("/{match_id}", response_model=MatchResponse)
async def get_match(match_id: str):
    match = await db["matches"].find_one({"_id": ObjectId(match_id)})
    if match:
        return match
    raise HTTPException(status_code=404, detail=f"Match with {match_id} not found")


@matches_router.post("", response_model=Response)
async def create_match(body: MatchCreate):
    match = body.model_dump()

    tournament_id = match["tournamentId"]
    tournament = await db["tournaments"].find_one({"_id": ObjectId(tournament_id)})
    if not tournament:
        raise HTTPException(
            status_code=404, detail=f"Tournament with id {tournament_id} does not exist. Match cannot be created"
        )

    created_match = await db["matches"].insert_one(match)
    if not created_match:
        raise HTTPException(status_code=500, detail="Match creation failed")

    return {"message": "Match created successfully"}


@matches_router.delete("/{match_id}", response_model=Response)
async def delete_match(match_id: str):
    deleted_count = db["matches"].delete_one({"_id": ObjectId(match_id)})
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Match not found")
    return {"message": "Match deleted successfully"}


@matches_router.patch("/{match_id}", response_model=MatchResponse)
async def update_match(
    match_id: str,
    body: MatchUpdate,
):
    body = body.model_dump(exclude_unset=True)
    match = await db["matches"].find_one({"_id": ObjectId(match_id)})
    if not match:
        raise HTTPException(status_code=404, detail=f"Match with id {match_id} not found")

    if match["status"] != MatchStatus.ONGOING and body["status"] == MatchStatus.ONGOING:
        body["startHour"] = datetime.now(app_timezone).replace(microsecond=0, tzinfo=None)
        body["endHour"] = None
    elif body["status"] == MatchStatus.FINISHED:
        end_hour = datetime.now(app_timezone).replace(microsecond=0, tzinfo=None)
        body["endHour"] = datetime.now(app_timezone).replace(microsecond=0, tzinfo=None)
        body["results"]["duration"] = (end_hour - match["startHour"]).seconds

    match_update = {**body, "lastUpdateDate": datetime.now(app_timezone).replace(microsecond=0, tzinfo=None)}
    result = await db["matches"].find_one_and_update(
        {"_id": ObjectId(match_id)}, {"$set": match_update}, return_document=True
    )

    await connection_manager.broadcast(MatchResponse.model_validate(result).model_dump(mode="json"))

    return result


@matches_router.patch("/{match_id}/results", response_model=MatchResponse)
async def update_match_results(
    match_id: str,
    body: MatchResultUpdate,
):
    body = body.model_dump(exclude_unset=True)
    match = await db["matches"].find_one({"_id": ObjectId(match_id)})
    if not match:
        raise HTTPException(status_code=404, detail=f"Match with id {match_id} not found")

    match_update = {"results": body, "lastUpdateDate": datetime.now(app_timezone).replace(microsecond=0, tzinfo=None)}
    result = await db["matches"].find_one_and_update(
        {"_id": ObjectId(match_id)}, {"$set": match_update}, return_document=True
    )
    return result


@matches_router.post("/{match_id}/verify-password", response_model=Response)
async def verify_password(match_id: str, body: MatchPassword):
    match = await db["matches"].find_one({"_id": ObjectId(match_id)})
    if match:
        match_players = [match["player1"], match["player2"]]
        tournament = await db["tournaments"].find_one({"_id": ObjectId(match["tournamentId"])})
        players_password = get_players_passwords(tournament["players"], match_players)
        if body.password in players_password:
            return {"message": "Password correct"}
        raise HTTPException(status_code=400, detail="Password not correct")
    raise HTTPException(status_code=404, detail=f"Match with {match_id} not found")
