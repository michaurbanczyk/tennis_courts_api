import os

from app.db.config import client
from app.seed.consts import FetchingStatus
from app.seed.utils import get_available_courts

current_directory = os.path.dirname(os.path.abspath(__file__))


def run_create_fetching_courts_data_status_table():
    available_courts = get_available_courts()
    tennis_db = client["tennis"]
    collection_name = "courtsDataStatus"

    if collection_name in tennis_db.list_collection_names():
        return

    documents = [
        {"clubName": ac["name"], "status": FetchingStatus.PREPARED, "startTime": "", "endTime": ""}
        for ac in available_courts
    ]

    courts_data_status_collection = client["tennis"]["courtsDataStatus"]
    courts_data_status_collection.insert_many(documents)
