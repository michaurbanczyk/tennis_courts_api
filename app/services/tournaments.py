import uuid

from app.models.tournaments import Tournament
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

    async def close(self):
        await self.repository.close()
