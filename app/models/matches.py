from datetime import datetime, timezone
from enum import StrEnum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.models.common import PyObjectId


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
    firstServe: str
    duration: str
    games: List[Result]

    @field_validator("duration", mode="before")
    def validate_duration(cls, value: int) -> str:
        if isinstance(value, int):
            hours, remainder = divmod(value, 3600)
            minutes = remainder // 60
            return f"{hours:01}h {minutes:02}min"
        else:
            return ""


class MatchResponse(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=str, alias="_id")
    player1: str = Field(...)
    player2: str = Field(...)
    plannedStartHour: str = Field(...)
    startHour: datetime | None = None
    endHour: datetime | None = None
    tournamentId: str = Field(...)
    clubName: str = Field(...)
    court: str = Field(...)
    status: Literal["Planned", "Ongoing", "Finished", "Archived", "Suspended"]
    results: MatchResults
    createdDate: datetime
    lastUpdateDate: datetime


class MatchCreate(BaseModel):
    player1: str = Field(...)
    player2: str = Field(...)
    plannedStartHour: str = Field(...)
    tournamentId: str = Field(...)
    clubName: str = Field(...)
    court: str = Field(...)
    results: MatchResults = Field(
        default_factory=lambda: MatchResults(firstServe="", duration="0", games=[{"player1": "0", "player2": "0"}])
    )
    status: Literal["Planned", "Ongoing", "Finished", "Archived", "Suspended"] = Field(
        default_factory=lambda: "Planned"
    )
    createdDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    lastUpdateDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))


class MatchUpdate(BaseModel):
    player1: str | None = None
    player2: str | None = None
    plannedStartHour: str | None = None
    tournamentId: str | None = None
    clubName: str | None = None
    results: MatchResults | None = None
    court: str | None = None
    status: Literal["Planned", "Ongoing", "Finished", "Archived", "Suspended"] | None = None


class MatchResultUpdate(BaseModel):
    firstServe: str | None = None
    duration: str | None = None
    games: List[Result] | None = None
