from datetime import datetime
from enum import StrEnum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.config import app_timezone
from app.models.common import PyObjectId


class MatchStatus(StrEnum):
    PLANNED = "Planned"
    ONGOING = "Ongoing"
    FINISHED = "Finished"


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
    plannedStartDate: datetime
    title: str | None = None
    subtitle: str | None = None
    startHour: datetime | None = None
    endHour: datetime | None = None
    transmissionLink: str | None = None
    tournamentId: str = Field(...)
    clubName: str = Field(...)
    court: str = Field(...)
    status: Literal["Planned", "Ongoing", "Finished"]
    results: MatchResults
    createdDate: datetime
    lastUpdateDate: datetime


class MatchCreate(BaseModel):
    player1: str = Field(...)
    player2: str = Field(...)
    plannedStartDate: datetime
    tournamentId: str = Field(...)
    title: str | None = None
    subtitle: str | None = None
    transmissionLink: str | None = None
    clubName: str = Field(...)
    court: str = Field(...)
    results: MatchResults = Field(
        default_factory=lambda: MatchResults(firstServe="", duration="0", games=[{"player1": "0", "player2": "0"}])
    )
    status: Literal["Planned", "Ongoing", "Finished"] = Field(default_factory=lambda: "Planned")
    createdDate: datetime = Field(
        default_factory=lambda: datetime.now(app_timezone).replace(microsecond=0, tzinfo=None)
    )
    lastUpdateDate: datetime = Field(
        default_factory=lambda: datetime.now(app_timezone).replace(microsecond=0, tzinfo=None)
    )


class MatchUpdate(BaseModel):
    player1: str | None = None
    player2: str | None = None
    plannedStartDate: datetime | None = None
    title: str | None = None
    subtitle: str | None = None
    transmissionLink: str | None = None
    clubName: str | None = None
    results: MatchResults | None = None
    court: str | None = None
    status: Literal["Planned", "Ongoing", "Finished"] | None = None


class MatchResultUpdate(BaseModel):
    firstServe: str | None = None
    duration: str | None = None
    games: List[Result] | None = None
