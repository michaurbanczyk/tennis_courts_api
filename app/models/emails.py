from pydantic import BaseModel


class EmailShareTheLink(BaseModel):
    addressList: list[str]
    tournamentLink: str
    tournamentTitle: str
