from pydantic import BaseModel
from typing import List, Literal, Optional


class Court(BaseModel):
    id: Optional[str] = None
    name: str
    type: Literal[
        "CLAY", "HARD", "GRASS", "ARTIFICIAL CLAY", "ARTIFICIAL GRASS", "CARPET", "CONCRETE", "OTHER"
    ]
    isSingleCourt: bool


class Tournament(BaseModel):
    id: Optional[str] = None
    name: str
    startDate: str
    endDate: str
    courts: List[Court]
    status: Literal[
        "PLANNED", "STARTED", "FINISHED"
    ] = "PLANNED"
    isArchived: bool = False


class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    courts: Optional[List[Court]] = None
