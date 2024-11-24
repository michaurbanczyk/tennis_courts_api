from pydantic import BaseModel


class Court(BaseModel):
    id: str
    name: str
    url: str
    occupancyUrl: str


class CourtResponse(BaseModel):
    courts: list[Court]


def to_courts_response(courts):
    return [
        {
            "id": str(court["_id"]),
            "name": court["name"],
            "url": court["url"],
            "occupancyUrl": court["occupancyUrl"],
        }
        for court in courts
    ]
