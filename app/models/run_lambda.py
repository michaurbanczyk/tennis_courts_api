from pydantic import BaseModel


class RunLambda(BaseModel):
    info: str
    status: str
