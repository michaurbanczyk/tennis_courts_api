from app.db.config import client


class ClubsRepository:
    def __init__(self):
        self.db_client = client
        # !TODO change the name of collection
        self.clubs_collection = self.db_client["tennis"]["allCourts"]

    def get_all(self):
        return self.clubs_collection.find()

    def get_by_id(self, ids):
        return self.clubs_collection.find({"_id": {"$in": ids}})

    def get_by_name(self, names):
        return self.clubs_collection.find({"name": {"$in": names}})
