from pydantic import BaseModel


class EmailShareTheLink(BaseModel):
    tournamentId: str
    tournamentLink: str
