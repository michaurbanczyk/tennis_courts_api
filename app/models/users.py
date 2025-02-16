from typing import Optional

from pydantic import BaseModel, Field

from app.models.common import PyObjectId


class UserBase(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=str, alias="_id")
    firstName: str
    lastName: str
    email: str
    phoneNumber: str


class CreateUser(UserBase):
    password: str


class UserResponse(UserBase):
    id: str


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    accessToken: str
    tokenType: str


class TokenData(BaseModel):
    username: Optional[str] = None
