from pydantic import BaseModel


class AvailableCourt(BaseModel):
    id: str
    date: str
    clubName: str
    url: str
    img: str
    courtName: str
    courtType: str
    duration: int
    start: str
    end: str
    isLeagueSlot: bool
    lastUpdated: str


class AvailableCourtResponse(BaseModel):
    availableCourts: list[AvailableCourt]


def to_available_courts_response(available_courts):
    return [
        {
            "id": str(ac["_id"]),
            "date": ac["date"],
            "clubName": ac["clubName"],
            "url": ac["url"],
            "img": ac["img"],
            "courtName": ac["courtName"],
            "courtType": ac["courtType"],
            "duration": ac["duration"],
            "start": ac["start"],
            "end": ac["end"],
            "isLeagueSlot": ac["isLeagueSlot"],
            "lastUpdated": ac["lastUpdated"],
        }
        for ac in available_courts
    ]
