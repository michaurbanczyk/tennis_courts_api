import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import FastMail, MessageSchema, MessageType
from jwt import InvalidTokenError

from app.config import conf
from app.db.config import db
from app.models.common import Response
from app.models.users import CreateUser, Login, UserBase, UserToken
from app.utils.hash import bcrypt, verify
from app.utils.oauth import oauth2_scheme
from app.utils.token import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    create_activation_token,
    verify_activation_token,
)

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


async def send_activation_email(subject: str, email_to: list[str], template_context: dict):
    message = MessageSchema(
        subject=subject, recipients=email_to, subtype=MessageType.html, template_body=template_context
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email.html")


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

    activation_token = create_activation_token(body.email)

    await send_activation_email(
        subject="Welcome in App Open",
        email_to=["contact@app-open.io", body.email],
        template_context={
            "body": {
                "tournament_title": "Example Tour",
                "tournament_password": activation_token,
                "tournament_link": f"https://{activation_token}",
            }
        },
    )

    return {"message": "User created successfully"}


@users_router.post("/login", response_model=UserToken)
async def login(user_login: Login):
    user_body = user_login.model_dump()
    user = await db["users"].find_one({"email": user_body["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify(user["password"], user_login.password):
        raise HTTPException(status_code=401, detail="Wrong password")
    access_token = create_access_token(data={"sub": user["email"]})
    return {**user, "accessToken": access_token, "tokenType": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid or expired token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await db["users"].find_one({"email": user_email})
    if not user:
        raise credentials_exception

    return user


@users_router.get("/me", response_model=UserBase)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    del current_user["password"]
    return current_user


@users_router.post("/activate")
async def activate(token: str):
    email = verify_activation_token(token)
    user = await db["users"].find_one({"email": email})
    if user:
        await db["users"].update_one({"_id": user["_id"]}, {"$set": {"isActive": True}})
        return {"message": "Account activated!"}
    raise HTTPException(status_code=404, detail="User not found")
