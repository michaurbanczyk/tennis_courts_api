from pydantic import BaseModel


class Club(BaseModel):
    id: str
    name: str
    url: str
    occupancyUrl: str
    img: str


class ClubsResponse(BaseModel):
    clubs: list[Club]


def to_clubs_response(clubs):
    return [
        {
            "id": str(club["_id"]),
            "name": club["name"],
            "url": club["url"],
            "occupancyUrl": club["occupancyUrl"],
            "img": club["img"],
        }
        for club in clubs
    ]
