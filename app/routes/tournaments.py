from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.models.tournaments import Tournament
from app.services.tournaments import TournamentService

tournaments_router = APIRouter(
    prefix="/tournaments",
    tags=["tournaments"],
)


def get_service():
    return TournamentService()


@tournaments_router.post("/")
async def create_tournament(tournament: Tournament, service: TournamentService = Depends(get_service)):
    try:
        return await service.create_tournament(tournament)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@tournaments_router.get("/", response_model=List[Tournament])
async def get_tournaments(service: TournamentService = Depends(get_service)):
    try:
        return await service.get_all_tournaments()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))