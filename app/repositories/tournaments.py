from bson import ObjectId

from app.db.config import client


class TournamentsRepository:
    def __init__(self):
        self.db_client = client
        self.tournaments_collection = self.db_client["tennis"]["tournaments"]

    async def create_tournament(self, tournament: dict):

        return await self.tournaments_collection.insert_one(tournament)

    async def get_tournament(self, tournament_id: str):
        tournament = await self.tournaments_collection.find_one({"_id": ObjectId(tournament_id)})
        return tournament

    async def get_tournaments(self):
        tournaments = await self.tournaments_collection.find().to_list(100)
        return [{**t, "id": str(t["_id"])} for t in tournaments]

    async def delete_tournament(self, tournament_id: str) -> int:
        result = await self.tournaments_collection.delete_one({"_id": ObjectId(tournament_id)})
        return result.deleted_count

    async def update_tournament(self, tournament_id: str, updated_data: dict) -> dict:
        result = await self.tournaments_collection.find_one_and_update(
            {"_id": ObjectId(tournament_id)}, {"$set": updated_data}, return_document=True
        )
        if result:
            result["id"] = str(result["_id"])
        return result

    async def close(self):
        await self.db_client.close()
