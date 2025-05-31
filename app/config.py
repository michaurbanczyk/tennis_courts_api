import os
from pathlib import Path

import pytz
from fastapi_mail import ConnectionConfig

DATETIME_FORMAT = "YYYY-MM-DDTHH:MM:SSZ"
app_timezone = pytz.timezone("Europe/Berlin")

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
    TEMPLATE_FOLDER=str(Path(__file__).resolve().parent.parent / "app" / "templates" / "email"),
)

conf_contact = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("EMAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("EMAIL_PASSWORD"),
    MAIL_FROM=os.environ.get("EMAIL_USERNAME"),
    MAIL_PORT=os.environ.get("EMAIL_PORT"),
    MAIL_SERVER=os.environ.get("EMAIL_SERVER"),
    MAIL_FROM_NAME="App Open",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=str(Path(__file__).resolve().parent.parent / "app" / "templates" / "contact_email"),
)
