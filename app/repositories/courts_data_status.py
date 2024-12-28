from pymongo import ReturnDocument

from app.db.config import client


class CourtsDataStatusRepository:
    def __init__(self):
        self.db_client = client
        self.courts_data_status_collection = self.db_client["tennis"]["courtsDataStatus"]

    def get(self, q: dict):
        return self.courts_data_status_collection.find_one(q)

    def get_all(self):
        return self.courts_data_status_collection.find()

    def update(self, filter_query: dict, update_data: dict):
        return self.courts_data_status_collection.find_one_and_update(
            filter_query, {"$set": update_data}, return_document=ReturnDocument.AFTER
        )
