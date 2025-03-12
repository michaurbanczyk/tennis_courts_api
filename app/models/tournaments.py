from datetime import datetime
from enum import StrEnum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.config import DATETIME_FORMAT
from app.models.common import PyObjectId


class TournamentStatus(StrEnum):
    PLANNED = "Planned"
    ONGOING = "Ongoing"
    FINISHED = "Finished"
    ARCHIVED = "Archived"
    SUSPENDED = "Suspended"


class Court(BaseModel):
    name: str = Field(...)
    type: Literal["Clay", "Hard", "Grass", "Artificial Clay", "Artificial Grass", "Carpet", "Concrete", "Other"] = (
        Field(...)
    )


class Player(BaseModel):
    name: str = Field(...)


class Location(BaseModel):
    clubName: str = Field(...)
    courts: List[Court]


class Organizer(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    phoneNumber: str = Field(...)


class Rules(BaseModel):
    maxNumberOfSets: int
    isLastSetSuperTiebreak: bool
    numberOfGamesInSet: int


class TournamentResponse(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=str, alias="_id")
    status: Literal["Planned", "Ongoing", "Archived", "Suspended", "Finished"]
    title: str = Field(...)
    subtitle: str | None = None
    isPrivate: bool
    password: str
    organizers: List[Organizer]
    rules: Rules
    startDate: datetime
    locations: List[Location]
    players: List[Player]
    createdBy: str
    createdDate: datetime
    lastUpdateDate: datetime

    @field_validator("startDate", mode="before")
    def validate_date_format(cls, value: str) -> datetime:
        if isinstance(value, datetime):
            return value
        try:
            return datetime.strptime(value, DATETIME_FORMAT)
        except ValueError:
            raise ValueError(f"Date format must be {DATETIME_FORMAT}, got {value}")


class TournamentCreate(BaseModel):
    title: str = Field(...)
    subtitle: str | None = None
    isPrivate: bool = False
    password: str = Field(..., min_length=5)
    organizers: List[Organizer]
    startDate: datetime
    locations: List[Location]
    players: List[Player]
    rules: Rules


class TournamentUpdate(BaseModel):
    title: str | None = None
    status: Literal["Planned", "Ongoing", "Archived", "Suspended", "Finished"] | None = None
    subtitle: str | None = None
    password: str | None = None
    organizers: List[Organizer] | None = None
    startDate: datetime | None = None
    isPrivate: bool | None = None
    locations: List[Location] | None = None
    players: List[Player] | None = None
    rules: Rules | None = None
