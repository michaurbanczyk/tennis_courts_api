from enum import StrEnum
from typing import List, Literal

from pydantic import BaseModel


class MatchStatus(StrEnum):
    PLANNED = "Planned"
    ONGOING = "Ongoing"
    FINISHED = "Finished"
    ARCHIVED = "Archived"
    SUSPENDED = "Suspended"


class Result(BaseModel):
    player1: str
    player2: str


class MatchResults(BaseModel):
    sets: Result
    games: List[Result]
    points: Result


class MatchBase(BaseModel):
    player1: str
    player2: str
    startDate: str
    endDate: str


class MatchResponse(MatchBase):
    id: str
    status: Literal["Planned", "Ongoing", "Finished", "Archived", "Suspended"]
    results: MatchResults

