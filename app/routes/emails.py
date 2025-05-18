import os
from pathlib import Path

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.db.config import db
from app.models.common import Response
from app.models.emails import EmailShareTheLink
from app.routes.users import get_current_user

emails_router = APIRouter(
    prefix="/emails",
    tags=["emails"],
)

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("EMAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("EMAIL_PASSWORD"),
    MAIL_FROM=os.environ.get("EMAIL_USERNAME"),
    MAIL_PORT=os.environ.get("EMAIL_PORT"),
    MAIL_SERVER=os.environ.get("EMAIL_SERVER"),
    MAIL_FROM_NAME="App Open",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=str(Path(__file__).resolve().parent.parent / "templates" / "email"),
)


async def send_email_async(subject: str, email_to: list[str], template_context: dict):
    message = MessageSchema(
        subject=subject, recipients=email_to, subtype=MessageType.html, template_body=template_context
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email.html")


@emails_router.post("/share-tournament-link", response_model=Response)
async def send_email_share_tournament_link(body: EmailShareTheLink, current_user: dict = Depends(get_current_user)):
    tournament = await db["tournaments"].find_one({"_id": ObjectId(body.tournamentId)})
    if not tournament:
        raise HTTPException(status_code=404, detail=f"Tournament with id {body.tournamentId} not found")

    errors_list = []

    for player in tournament["players"]:
        try:
            if player["email"]:
                await send_email_async(
                    subject=f"Welcome in {tournament['title']} tennis tournament by App Open",
                    email_to=[player["email"]],
                    template_context={
                        "body": {
                            "tournament_title": tournament["title"],
                            "tournament_password": player["password"],
                            "tournament_link": body.tournamentLink,
                        }
                    },
                )
        except Exception:
            errors_list.append(player["name"])

    if errors_list:
        raise HTTPException(status_code=500, detail=f"Email has not been delivered to: {', '.join(errors_list)}.")

    return {"message": "Email has been sent successfully!"}
