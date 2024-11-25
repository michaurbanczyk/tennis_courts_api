from pydantic import BaseModel


class AvailableCourt(BaseModel):
    id: str
    name: str
    courts: list
    lastUpdated: str


class AvailableCourtResponse(BaseModel):
    availableCourts: list[AvailableCourt]


def to_available_courts_response(available_courts):
    return [
        {
            "id": str(ac["_id"]),
            "name": ac["name"],
            "courts": ac["courts"],
            "lastUpdated": ac["lastUpdated"],
        }
        for ac in available_courts
    ]
