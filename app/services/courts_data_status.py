from fastapi import HTTPException

from app.models.courts_data_status import (
    CourtsDataStatusUpdate,
    to_courts_data_status_response,
)
from app.repositories.courts_data_status import CourtsDataStatusRepository


class CourtsDataService:
    def __init__(self, courts_data_status_repository: CourtsDataStatusRepository = CourtsDataStatusRepository()):
        self.courts_data_status_repository = courts_data_status_repository

    def get_all(self):
        courts_data_status = self.courts_data_status_repository.get_all()

        return to_courts_data_status_response(courts_data_status) if courts_data_status else []

    def get(self, club_name: str):
        court_data_status = self.courts_data_status_repository.get({"clubName": club_name})

        return court_data_status

    def update_courts_data_service(self, body: CourtsDataStatusUpdate):
        club_name = body.clubName

        court_data_status = self.courts_data_status_repository.get({"clubName": club_name})
        if not court_data_status:
            raise HTTPException(status_code=404, detail="Club Name not found")

        update_data = self._prepare_update_data(body)

        if update_data:
            updated_entry = self.courts_data_status_repository.update({"clubName": club_name}, update_data)
            if not updated_entry:
                raise ValueError(f"Failed to update entry for clubName: {club_name}")

            courts_data_status = self.courts_data_status_repository.get_all()

            return to_courts_data_status_response(courts_data_status) if courts_data_status else []

        courts_data_status = self.courts_data_status_repository.get_all()

        return to_courts_data_status_response(courts_data_status) if courts_data_status else []

    @staticmethod
    def _prepare_update_data(body: CourtsDataStatusUpdate):
        update_data = {}
        if body.status is not None:
            update_data["status"] = body.status
        if body.startTime is not None:
            update_data["startTime"] = body.startTime
        if body.endTime is not None:
            update_data["endTime"] = body.endTime

        return update_data
