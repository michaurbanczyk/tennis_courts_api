from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException

from app.db.config import db
from app.models.common import Response
from app.models.matches import MatchCreate, MatchResponse

matches_router = APIRouter(
    prefix="/matches",
    tags=["matches"],
)


@matches_router.get("/", response_model=List[MatchResponse])
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


@matches_router.post("/", response_model=Response)
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


# @matches_router.patch("/{match_id}/results", response_model=MatchResponse)
# async def update_results(match_id: str, results: MatchResults, service: MatchService = Depends(get_service)):
#     updated_match = await service.update_results(match_id, results)
#     if not updated_match:
#         raise HTTPException(status_code=404, detail="Match not found")
#     return updated_match
