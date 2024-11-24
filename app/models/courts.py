from pydantic import BaseModel


class Court(BaseModel):
    id: str
    name: str
    url: str
    occupancyUrl: str


class CourtResponse(BaseModel):
    courts: list[Court]
