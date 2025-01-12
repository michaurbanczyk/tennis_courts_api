from pydantic import BaseModel


class Response(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
    code: str
    message: str
