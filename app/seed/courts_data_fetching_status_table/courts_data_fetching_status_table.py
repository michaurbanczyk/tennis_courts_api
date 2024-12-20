import os
from enum import StrEnum

from app.db.config import client
from app.seed.utils import get_available_courts

current_directory = os.path.dirname(os.path.abspath(__file__))


class FetchingStatus(StrEnum):
    STARTED = "Started"
    SUCCESS = "Success"
    ERROR = "Error"
    IN_PROGRESS = "In Progress"
    FINISHED = "Finished"
    PREPARED = "Prepared"


def run_create_fetching_courts_data_status_table():
    available_courts = get_available_courts()
    documents = [
        {"clubName": ac["name"], "status": FetchingStatus.PREPARED, "startTime": "", "endTime": ""}
        for ac in available_courts
    ]
    courts_data_status_collection = client["tennis"]["courtsDataStatus"]
    courts_data_status_collection.drop()
    courts_data_status_collection.insert_many(documents)
