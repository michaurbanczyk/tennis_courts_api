from enum import StrEnum
from typing import List, Literal, Optional

from pydantic import BaseModel


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


class Configuration(BaseModel):
    numberOfGames: int
    isAdvantage: bool = True


class Organizer(BaseModel):
    name: str
    email: str
    phoneNumber: str


class TournamentBase(BaseModel):
    organizers: List[Organizer]
    title: str
    subtitle: str
    startDate: str
    endDate: str
    locations: List[Location]
    players: List[Player]
    configuration: Configuration


class TournamentResponse(TournamentBase):
    id: str
    status: Literal["Planned", "Ongoing", "Archived", "Suspended", "Finished"]
    createdDate: str
    lastUpdateDate: str


class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    courts: Optional[List[Court]] = None
