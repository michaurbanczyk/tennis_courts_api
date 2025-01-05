from typing import List

from fastapi import APIRouter, HTTPException, Depends

from app.config import websocket_manager
from app.models.common import Response
from app.models.matches import MatchResults, MatchResponse, MatchBase
from app.services.matches import MatchService

matches_router = APIRouter(
    prefix="/matches",
    tags=["matches"],
)


def get_service():
    return MatchService(websocket_manager)


@matches_router.get("/{match_id}", response_model=MatchResponse)
async def get_match(match_id: str, service: MatchService = Depends(get_service)):
    match = await service.get_match(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@matches_router.get("/", response_model=List[MatchResponse])
async def get_matches(service: MatchService = Depends(get_service)):
    matches = await service.get_matches()
    return matches


@matches_router.post("/", response_model=MatchResponse)
async def create_match(match: MatchBase, service: MatchService = Depends(get_service)):
    try:
        return await service.create_match(match)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@matches_router.delete("/{match_id}", response_model=Response)
async def delete_match(match_id: str, service: MatchService = Depends(get_service)):
    deleted_count = await service.delete_match(match_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Match not found")
    return {"message": "Match deleted successfully"}


@matches_router.patch("/{match_id}/results", response_model=MatchResponse)
async def update_results(match_id: str, results: MatchResults, service: MatchService = Depends(get_service)):
    updated_match = await service.update_results(match_id, results)
    if not updated_match:
        raise HTTPException(status_code=404, detail="Match not found")
    return updated_match
