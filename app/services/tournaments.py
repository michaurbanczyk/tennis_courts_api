import uuid

from app.models.tournaments import Tournament, TournamentUpdate
from app.repositories.tournaments import TournamentsRepository


class TournamentService:
    def __init__(self):
        self.repository = TournamentsRepository()

    async def create_tournament(self, tournament: Tournament) -> dict:
        tournament_dict = tournament.model_dump()

        for court in tournament_dict["courts"]:
            court["id"] = str(uuid.uuid4())

        return await self.repository.create_tournament(tournament_dict)

    async def get_all_tournaments(self) -> list:
        return await self.repository.get_all_tournaments()

    async def delete_tournament(self, tournament_id: str) -> int:
        return await self.repository.delete_tournament(tournament_id)

    async def update_tournament(self, tournament_id: str, updated_data: TournamentUpdate):
        updated_data_dict = updated_data.model_dump(exclude_unset=True)

        return await self.repository.update_tournament(tournament_id, updated_data_dict)

    async def close(self):
        await self.repository.close()
