
from pydantic import BaseModel

class Result(BaseModel):
    player1: int
    player2: int


class MatchResults(BaseModel):
    sets: Result
    games: Result
    points: Result


class MatchBase(BaseModel):
    player1: str
    player2: str
    startDate: str
    endDate: str


class MatchResponse(MatchBase):
    id: str
    results: MatchResults

