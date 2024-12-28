from fastapi import APIRouter

from app.models.courts_data_status import (
    CourtsDataStatusResponse,
    CourtsDataStatusUpdate,
)
from app.services.courts_data_status import CourtsDataService

courts_data_status = APIRouter(
    prefix="/courts-data-status",
    tags=["courts-data-status"],
)


@courts_data_status.get("/", response_model=CourtsDataStatusResponse)
def get_courts_data_status():

    courts_data_service = CourtsDataService()
    courts_data = courts_data_service.get_all()

    return {"courtsDataStatus": courts_data}


@courts_data_status.patch("/update", response_model=CourtsDataStatusResponse)
def update_courts_data_status(body: CourtsDataStatusUpdate):

    courts_data_service = CourtsDataService()
    courts_data = courts_data_service.update_courts_data_service(body)

    return {"courtsDataStatus": courts_data}
