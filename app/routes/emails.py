import os

from fastapi import APIRouter, Depends, HTTPException
from sendgrid import Mail, SendGridAPIClient

from app.models.common import Response
from app.models.emails import EmailShareTheLink
from app.routes.users import get_current_user

emails_router = APIRouter(
    prefix="/emails",
    tags=["emails"],
)

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS", "")
SENDGRID_ACCESS_KEY = os.environ.get("SENDGRID_ACCESS_KEY", "")


@emails_router.post("/share-tournament-link", response_model=Response)
async def send_email(body: EmailShareTheLink, current_user: dict = Depends(get_current_user)):
    body = body.model_dump()
    if not body['addressList'] or not body["tournamentLink"]:
        raise HTTPException(status_code=400, detail="Empty email address list or transmission link")

    message = Mail(
        from_email=EMAIL_ADDRESS,
        to_emails=body['addressList'],
        subject=f"Join the {body['tournamentTitle']} tournament in App Open",
        html_content=f'<strong>{body['tournamentLink']}</strong>')
    try:
        sg = SendGridAPIClient(SENDGRID_ACCESS_KEY)
        response = sg.send(message)
        if response.status_code != 202:
            raise HTTPException(status_code=500, detail="Error with sending emails")
        return {"message": "Emails have been sent successfully!"}
    except Exception:
        raise HTTPException(status_code=500, detail="Error with sending emails")
