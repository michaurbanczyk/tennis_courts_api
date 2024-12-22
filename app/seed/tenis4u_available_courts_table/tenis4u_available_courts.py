from app.db.config import client
from app.seed.utils import get_available_courts


def run_get_tenis4u_available_courts():
    available_courts = get_available_courts()
    tennis_db = client["tennis"]

    collection_name = "courts"

    if collection_name in tennis_db.list_collection_names():
        return

    all_tennis_courts_collection = client["tennis"][collection_name]
    all_tennis_courts_collection.insert_many(available_courts)
