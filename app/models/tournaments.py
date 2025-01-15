from datetime import datetime
from enum import StrEnum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.config import DATETIME_FORMAT


class TournamentStatus(StrEnum):
    PLANNED = "Planned"
    ONGOING = "Ongoing"
    FINISHED = "Finished"
    ARCHIVED = "Archived"
    SUSPENDED = "Suspended"


class Court(BaseModel):
    name: str
    type: Literal["Clay", "Hard", "Grass", "Artificial Clay", "Artificial Grass", "Carpet", "Concrete", "Other"]


class Player(BaseModel):
    name: str


class Location(BaseModel):
    clubName: str
    courts: List[Court]


class Organizer(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    phoneNumber: str = Field(...)


class TournamentBase(BaseModel):
    organizers: List[Organizer]
    title: str = Field(...)
    subtitle: Optional[str] = None
    startDate: datetime
    locations: List[Location]
    players: List[Player]

    @field_validator("startDate", mode="before")
    def validate_date_format(cls, value: str) -> datetime:
        if isinstance(value, datetime):
            return value
        try:
            return datetime.strptime(value, DATETIME_FORMAT)
        except ValueError:
            raise ValueError(f"Date format must be {DATETIME_FORMAT}, got {value}")


class TournamentResponse(TournamentBase):
    id: str
    status: Literal["Planned", "Ongoing", "Archived", "Suspended", "Finished"]
    createdDate: datetime
    lastUpdateDate: datetime


class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    courts: Optional[List[Court]] = None
