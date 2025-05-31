from pydantic import BaseModel


class EmailShareTheLink(BaseModel):
    tournamentId: str
    tournamentLink: str


class ContactEmail(BaseModel):
    firstName: str
    lastName: str
    email: str
    message: str
