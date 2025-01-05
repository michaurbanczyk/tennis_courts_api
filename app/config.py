import os

import pytz

from app.websocket_manager import WebSocketManager

LAMBDA_RUN_ENDPOINT = os.getenv("LAMBDA_RUN_ENDPOINT", "")
LAMBDA_RUN_INTERVAL = os.getenv("LAMBDA_RUN_INVERVAL", "2")
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

timezone = pytz.timezone("Europe/Berlin")
websocket_manager = WebSocketManager()