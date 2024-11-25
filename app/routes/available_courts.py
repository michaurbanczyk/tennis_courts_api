from fastapi import APIRouter, Request

from app.models.available_courts import AvailableCourtResponse
from app.services.available_courts import AvailableCourtsService

available_courts_router = APIRouter(
    prefix="/available-courts",
    tags=["available-courts"],
)


@available_courts_router.get("/", response_model=AvailableCourtResponse)
def get_available_courts(request: Request):
    query_params = request.query_params

    available_courts_service = AvailableCourtsService()
    all_available_courts = available_courts_service.get_all(query_params)

    return {"availableCourts": all_available_courts}


@available_courts_router.get("/by-dates")
def get_available_courts_by_dates(request: Request):
    query_params = request.query_params

    available_courts_service = AvailableCourtsService()
    all_available_courts_by_dates = available_courts_service.get_all_by_dates(query_params)

    return {"availableCourts": all_available_courts_by_dates}
