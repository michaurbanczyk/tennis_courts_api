from app.models.users import CreateUser
from app.repositories.users import UsersRepository
from app.utils.hash import bcrypt


class UserService:
    def __init__(self):
        self.repository = UsersRepository()

    async def create_user(self, user: CreateUser) -> dict:
        user_data = user.model_dump()
        user_data["password"] = bcrypt(user_data["password"])
        created_user = await self.repository.create_user(user_data)
        user_data["id"] = str(created_user.inserted_id)
        return user_data

    async def get_user_by_username(self, username: str):
        user = await self.repository.get_user_by_username(username)
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]

        return user
