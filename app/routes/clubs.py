from fastapi import APIRouter, Request

from app.models.clubs import ClubsResponse
from app.services.clubs import ClubsService

clubs_router = APIRouter(
    prefix="/clubs",
    tags=["clubs"],
)


@clubs_router.get("/", response_model=ClubsResponse)
def get_clubs(request: Request):
    query_params = request.query_params

    clubs_service = ClubsService()
    all_clubs = clubs_service.get_all(query_params)

    return {"clubs": all_clubs}
