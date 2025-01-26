from bson import ObjectId

from app.db.config import client


class UsersRepository:
    def __init__(self):
        self.db_client = client
        self.users_collection = self.db_client["tennis"]["users"]

    async def create_user(self, user: dict):
        return await self.users_collection.insert_one(user)

    async def get_user(self, user_id: str):
        user = await self.users_collection.find_one({"_id": ObjectId(user_id)})
        return user

    async def get_user_by_username(self, username: str):
        user = await self.users_collection.find_one({"username": username})
        return user

    async def get_users(self):
        users = await self.users_collection.find().to_list(100)
        return [{**u, "id": str(u["_id"])} for u in users]
