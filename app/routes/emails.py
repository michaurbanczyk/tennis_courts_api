from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import FastMail, MessageSchema, MessageType

from app.config import conf, conf_contact
from app.db.config import db
from app.models.common import Response
from app.models.emails import ContactEmail, EmailShareTheLink
from app.routes.users import get_current_user

emails_router = APIRouter(
    prefix="/emails",
    tags=["emails"],
)


async def send_email_async(subject: str, email_to: list[str], template_context: dict, conf_type: str = "contact"):
    message = MessageSchema(
        subject=subject, recipients=email_to, subtype=MessageType.html, template_body=template_context
    )

    if conf_type == "contact":
        fm = FastMail(conf_contact)
    else:
        fm = FastMail(conf)

    await fm.send_message(message, template_name="contact_email.html" if conf_type == "contact" else "email.html")


@emails_router.post("/share-tournament-link", response_model=Response)
async def send_email_share_tournament_link(body: EmailShareTheLink, current_user: dict = Depends(get_current_user)):
    tournament = await db["tournaments"].find_one({"_id": ObjectId(body.tournamentId)})
    if not tournament:
        raise HTTPException(status_code=404, detail=f"Tournament with id {body.tournamentId} not found")

    errors_list = []

    for player in tournament["players"]:
        try:
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


@emails_router.post("/contact", response_model=Response)
async def send_contact_email(body: ContactEmail):
    try:
        await send_email_async(
            subject="App open Contact Form",
            email_to=["contact@app-open.io"],
            template_context={
                "body": {
                    "first_name": body.firstName,
                    "last_name": body.lastName,
                    "email": body.email,
                    "message": body.message,
                }
            },
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Email has not been delivered to!")

    return {"message": "Email sent successfully!"}
