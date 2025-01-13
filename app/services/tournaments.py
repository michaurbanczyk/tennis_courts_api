import datetime

from app.models.tournaments import TournamentBase, TournamentStatus, TournamentUpdate
from app.repositories.tournaments import TournamentsRepository


class TournamentService:
    def __init__(self):
        self.repository = TournamentsRepository()

    async def create_tournament(self, tournament: TournamentBase) -> dict:
        current_time = datetime.datetime.now(datetime.timezone.utc)
        tournament_dict = {
            **tournament.model_dump(),
            "status": TournamentStatus.PLANNED,
            "createdDate": current_time,
            "lastUpdateDate": current_time,
        }
        result = await self.repository.create_tournament(tournament_dict)
        tournament_dict["id"] = str(result.inserted_id)

        return tournament_dict

    async def get_tournament(self, tournament_id: str):
        tournament = await self.repository.get_tournament(tournament_id)
        if tournament:
            tournament["id"] = str(tournament["_id"])
            del tournament["_id"]
        return tournament

    async def get_tournaments(self) -> list:
        return await self.repository.get_tournaments()

    async def delete_tournament(self, tournament_id: str) -> int:
        return await self.repository.delete_tournament(tournament_id)

    async def update_tournament(self, tournament_id: str, updated_data: TournamentUpdate):
        updated_data_dict = updated_data.model_dump(exclude_unset=True)

        return await self.repository.update_tournament(tournament_id, updated_data_dict)

    async def close(self):
        await self.repository.close()
