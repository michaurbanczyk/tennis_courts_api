from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt

from app.db.config import db
from app.models.common import Response
from app.models.users import CreateUser, Login, Token
from app.utils.hash import bcrypt, verify
from app.utils.oauth import oauth2_scheme
from app.utils.token import ALGORITHM, SECRET_KEY, create_access_token

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@users_router.post("/register", response_model=Response)
async def register(body: CreateUser):
    user_body = body.model_dump()
    user = await db["users"].find_one({"email": user_body["email"]})
    if user:
        raise HTTPException(status_code=409, detail="User with this email address already exists")
    user_body["password"] = bcrypt(user_body["password"])
    created_user = await db["users"].insert_one(user_body)
    if not created_user:
        raise HTTPException(status_code=500, detail="User creation failed")
    return {"message": "User created successfully"}


@users_router.post("/login", response_model=Token)
async def login(user_login: Login):
    user_body = user_login.model_dump()
    user = await db["users"].find_one({"email": user_body["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify(user["password"], user_login.password):
        raise HTTPException(status_code=401, detail="Wrong password or username")
    access_token = create_access_token(data={"sub": user["email"]})
    return {"accessToken": access_token, "tokenType": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid or expired token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db["users"].find_one({"email": user_email})
    if not user:
        raise credentials_exception

    return {"user_email": user_email}


@users_router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["user_email"]}
