from app.db.config import client


class CourtsRepository:
    def __init__(self):
        self.db_client = client
        self.all_tennis_courts_collection = self.db_client["tennis"]["all_courts"]

    async def get_all(self):
        return self.all_tennis_courts_collection.find()
