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
    games: List[Result]


class MatchBase(BaseModel):
    player1: str
    player2: str
    startHour: str
    tournamentId: str
    clubName: str
    court: str


class MatchResponse(MatchBase):
    id: str
    status: Literal["Planned", "Ongoing", "Finished", "Archived", "Suspended"]
    results: MatchResults
