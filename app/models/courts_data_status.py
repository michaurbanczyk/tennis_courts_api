from typing import Optional

from pydantic import BaseModel

from app.models.run_lambda import RunLambdaStatusEnum


class CourtDataStatus(BaseModel):
    id: str
    clubName: str
    status: str
    startTime: str
    endTime: str


class CourtsDataStatusResponse(BaseModel):
    courtsDataStatus: list[CourtDataStatus]


class CourtsDataStatusUpdate(BaseModel):
    clubName: str
    status: Optional[RunLambdaStatusEnum] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None


def to_courts_data_status_response(courts_data):
    return [
        {
            "id": str(court["_id"]),
            "clubName": court["clubName"],
            "status": court["status"],
            "startTime": court["startTime"],
            "endTime": court["endTime"],
        }
        for court in courts_data
    ]
