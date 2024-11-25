from app.db.config import client


class CourtsRepository:
    def __init__(self):
        self.db_client = client
        self.all_tennis_courts_collection = self.db_client["tennis"]["allCourts"]

    def get_all(self):
        return self.all_tennis_courts_collection.find()

    def get_by_id(self, ids):
        return self.all_tennis_courts_collection.find({"_id": {"$in": ids}})

    def get_by_name(self, names):
        return self.all_tennis_courts_collection.find({"name": {"$in": names}})
