from fastapi import APIRouter, Request

from app.models.courts import CourtResponse
from app.services.courts import CourtsService

courts_router = APIRouter(
    prefix="/courts",
    tags=["courts"],
)


@courts_router.get("/", response_model=CourtResponse)
def get_courts(request: Request):
    query_params = request.query_params

    courts_service = CourtsService()
    all_courts = courts_service.get_all(query_params)

    return {"courts": all_courts}
