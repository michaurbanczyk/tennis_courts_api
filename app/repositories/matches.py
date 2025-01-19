from typing import Optional

from bson import ObjectId

from app.db_connection import db_client
from app.models.matches import MatchStatus


class MatchRepository:
    def __init__(self):
        self.db_client = db_client.db_client
        self.matches_collection = self.db_client["tennis"]["matches"]

    async def create_match(self, match: dict) -> dict:
        match.update(
            status=MatchStatus.PLANNED,
            results={
                "sets": {
                    "player1": "0",
                    "player2": "0",
                },
                "games": [
                    {
                        "player1": "0",
                        "player2": "0",
                    },
                ],
                "points": {
                    "player1": "0",
                    "player2": "0",
                },
            },
        )
        results = await self.matches_collection.insert_one(match)
        match["id"] = str(results.inserted_id)
        return match

    async def get_matches(self):
        matches = await self.matches_collection.find().to_list(100)
        return [{**m, "id": str(m["_id"])} for m in matches]

    async def get_match(self, match_id: str) -> Optional[dict]:
        return await self.matches_collection.find_one({"_id": ObjectId(match_id)})

    async def update_match(self, match_id: str, update_data: dict) -> Optional[dict]:
        return await self.matches_collection.find_one_and_update(
            {"_id": match_id}, {"$set": update_data}, return_document=True
        )

    async def delete_match(self, match_id: str) -> int:
        result = await self.matches_collection.delete_one({"_id": ObjectId(match_id)})
        return result.deleted_count

    async def update_results(self, match_id: str, results_data: dict) -> Optional[dict]:
        return await self.matches_collection.find_one_and_update(
            {"_id": ObjectId(match_id)}, {"$set": {"results": results_data}}, return_document=True
        )

    async def close(self):
        await self.db_client.close()
