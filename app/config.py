import pytz

from app.websocket_manager import WebSocketManager

DATETIME_FORMAT = "%Y-%m-%dT%H:%M"
timezone = pytz.timezone("Europe/Berlin")

websocket_manager = WebSocketManager()
