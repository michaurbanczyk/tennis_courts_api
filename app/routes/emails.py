import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

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
    if not body.addressList or not body.tournamentLink:
        raise HTTPException(status_code=400, detail="Empty email address list or transmission link")

    try:
        await send_email_async(
            subject=f"Welcome in {body.tournamentTitle} powered by App Open",
            email_to=body.addressList,
            template_context={"body": {"title": "Hello World", "name": "John Doe"}},
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Email sending has been failed.")

    return {"message": "Email has been sent successfully!"}
