from fastapi import APIRouter, Request

from app.models.courts import CourtsResponse
from app.services.courts import CourtsService

courts_router = APIRouter(
    prefix="/courts",
    tags=["courts"],
)


@courts_router.get("/", response_model=CourtsResponse)
def get_courts(request: Request):
    query_params = request.query_params

    courts_service = CourtsService()
    courts = courts_service.get_all(query_params)

    return {"courts": courts}
