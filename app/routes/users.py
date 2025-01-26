from fastapi import APIRouter, Depends, HTTPException

from app.models.users import CreateUser, Login, Token, UserResponse
from app.services.users import UserService
from app.utils.hash import verify
from app.utils.token import create_access_token

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def get_service():
    return UserService()


@users_router.post("/register", response_model=UserResponse)
async def register(user: CreateUser, service: UserService = Depends(get_service)):
    user = await service.get_user_by_email(user.email)
    if user:
        raise HTTPException(status_code=409, detail="User with this email address already exists")
    return await service.create_user(user)


@users_router.post("/login", response_model=Token)
async def login(user_login: Login, service: UserService = Depends(get_service)):
    user = await service.get_user_by_email(user_login.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify(user["password"], user_login.password):
        raise HTTPException(status_code=401, detail="Wrong password or username")
    access_token = create_access_token(data={"sub": user["email"]})
    return {"accessToken": access_token, "tokenType": "bearer"}
