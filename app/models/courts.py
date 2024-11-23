from pydantic import BaseModel


class Court(BaseModel):
    id: str
    name: str
    freeSlots: list[dict]
    lastUpdated: str


class CourtResponse(BaseModel):
    courts: list[Court]
