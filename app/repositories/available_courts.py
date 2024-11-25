from app.db.config import client


class AvailableCourtsRepository:
    def __init__(self):
        self.db_client = client
        self.courts_availability = self.db_client["tennis"]["courtsAvailability"]

    def get_all(self):
        return self.courts_availability.find()

    def get_by_id(self, ids):
        return self.courts_availability.find({"_id": {"$in": ids}})

    def get_by_name(self, names):
        return self.courts_availability.find({"name": {"$in": names}})
