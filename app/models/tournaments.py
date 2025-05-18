from datetime import datetime
from enum import StrEnum
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.config import DATETIME_FORMAT, app_timezone
from app.models.common import PyObjectId


class TournamentStatus(StrEnum):
    PLANNED = "Planned"
    ONGOING = "Ongoing"
    FINISHED = "Finished"
    ARCHIVED = "Archived"
    SUSPENDED = "Suspended"


class Court(BaseModel):
    id: str = Field(default="")
    name: str = Field(...)
    type: Literal["Clay", "Hard", "Grass", "Artificial Clay", "Artificial Grass", "Carpet", "Concrete", "Other"] = (
        Field(...)
    )


class Player(BaseModel):
    id: str = Field(default="")
    name: str = Field(...)
    email: str = Field(default="")
    # password: str = Field(default="") this should be not returned for safety purposes,
    # there will be a special endpoint to do this


class PlayerWithPasswords(Player):
    password: str


class Location(BaseModel):
    id: str = Field(default="")
    clubName: str = Field(...)
    courts: List[Court]


class TournamentResponse(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=str, alias="_id")
    status: Literal["Planned", "Ongoing", "Finished"]
    title: str = Field(...)
    subtitle: str | None = None
    startDate: datetime
    locations: List[Location]
    players: List[Player]
    createdBy: PyObjectId = Field(default_factory=str, alias="createdBy")
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


class PaginatedTournamentResponse(BaseModel):
    tournaments: List[TournamentResponse]
    total: int


class TournamentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(...)
    subtitle: str | None = None
    status: TournamentStatus = Field(default=TournamentStatus.PLANNED)
    startDate: datetime
    locations: List[Location]
    players: List[Player]
    createdDate: datetime = Field(
        default_factory=lambda: datetime.now(app_timezone).replace(microsecond=0, tzinfo=None)
    )
    lastUpdateDate: datetime = Field(
        default_factory=lambda: datetime.now(app_timezone).replace(microsecond=0, tzinfo=None)
    )

    @field_validator("locations")
    @classmethod
    def validate_locations_not_empty(cls, locations: List[Location]) -> List[Location]:
        if not locations:
            raise ValueError("At least one location is required.")
        return locations

    @field_validator("players")
    @classmethod
    def validate_players_not_empty(cls, players: List[Player]) -> List[Player]:
        if not players:
            raise ValueError("At least one player is required.")
        return players


class TournamentUpdate(BaseModel):
    title: str | None = None
    status: Literal["Planned", "Ongoing", "Finished"] | None = None
    subtitle: str | None = None
    startDate: datetime | None = None
    locations: List[Location] | None = None
    players: List[Player] | None = None
