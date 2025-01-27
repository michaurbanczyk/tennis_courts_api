from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.models.common import Response
from app.models.tournaments import TournamentBase, TournamentResponse
from app.services.tournaments import TournamentService

tournaments_router = APIRouter(
    prefix="/tournaments",
    tags=["tournaments"],
)


def get_service():
    return TournamentService()


@tournaments_router.get("/", response_model=List[TournamentResponse])
async def get_tournaments(service: TournamentService = Depends(get_service)):
    try:
        return await service.get_tournaments()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@tournaments_router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(tournament_id: str, service: TournamentService = Depends(get_service)):
    try:
        return await service.get_tournament(tournament_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@tournaments_router.post("/", response_model=TournamentResponse)
async def create_tournament(tournament: TournamentBase, service: TournamentService = Depends(get_service)):
    try:
        return await service.create_tournament(tournament)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@tournaments_router.delete("/{tournament_id}", response_model=Response)
async def delete_tournament(tournament_id: str, service: TournamentService = Depends(get_service)):
    try:
        deleted_count = await service.delete_tournament(tournament_id)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Tournament not found")
        return {"message": "Tournament deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#
#
# @tournaments_router.patch("/{tournament_id}", response_model=Tournament)
# async def update_tournament(
#     tournament_id: str,
#     updated_data: TournamentUpdate,
#     service: TournamentService = Depends(get_service)
# ):
#     try:
#         updated_tournament = await service.update_tournament(tournament_id, updated_data)
#         if not updated_tournament:
#             raise HTTPException(status_code=404, detail="Tournament not found")
#         return updated_tournament
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
