from pydantic import BaseModel


class Court(BaseModel):
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


class CourtsResponse(BaseModel):
    courts: list[Court]


def to_courts_response(courts):
    return [
        {
            "id": str(court["_id"]),
            "date": court["date"],
            "clubName": court["clubName"],
            "url": court["url"],
            "img": court["img"],
            "courtName": court["courtName"],
            "courtType": court["courtType"],
            "duration": court["duration"],
            "start": court["start"],
            "end": court["end"],
            "isLeagueSlot": court["isLeagueSlot"],
            "lastUpdated": court["lastUpdated"],
        }
        for court in courts
    ]
