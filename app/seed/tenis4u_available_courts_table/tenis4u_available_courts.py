from app.db.config import client
from app.seed.utils import get_available_courts


def run_get_tenis4u_available_courts():
    available_courts = get_available_courts()
    all_tennis_courts_collection = client["tennis"]["clubs"]
    all_tennis_courts_collection.drop()
    all_tennis_courts_collection.insert_many(available_courts)
