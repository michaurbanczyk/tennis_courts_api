from app.repositories.courts import CourtsRepository


class CourtsService:
    def __init__(self, courts_repository: CourtsRepository = CourtsRepository()):
        self.courts_repository = courts_repository

    async def get_all(self):
        courts = await self.courts_repository.get_all()
        all_courts = [
            {
                "id": str(court["_id"]),
                "name": court["name"],
                "url": court["url"],
                "occupancyUrl": court["occupancyUrl"],
            }
            for court in courts
        ]

        return all_courts
