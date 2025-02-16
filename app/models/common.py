from typing import Annotated

from pydantic import BaseModel, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class Response(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
    code: str
    message: str
