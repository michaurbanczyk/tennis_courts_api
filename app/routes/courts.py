from fastapi import APIRouter

from app.models.courts import CourtResponse
from app.services.courts import CourtsService

courts_router = APIRouter(
    prefix="/courts",
    tags=["courts"],
)


@courts_router.get("/", response_model=CourtResponse)
async def courts():

    courts_service = CourtsService()
    get_all_courts = await courts_service.get_all()

    return {"courts": get_all_courts}
