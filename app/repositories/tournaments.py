from app.db.config import client


class TournamentsRepository:
    def __init__(self):
        self.db_client = client
        self.tournaments_collection = self.db_client["tennis"]["tournaments"]

    async def create_tournament(self, tournament: dict) -> dict:
        result = await self.tournaments_collection.insert_one(tournament)
        tournament["_id"] = str(result.inserted_id)
        return tournament

    async def get_all_tournaments(self) -> list:
        tournaments = await self.tournaments_collection.find().to_list(100)
        return [{**t, "id": str(t["_id"])} for t in tournaments]

    async def close(self):
        await self.db_client.close()
