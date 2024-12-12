from app.models.courts import to_courts_response
from app.repositories.courts import CourtsRepository


class CourtsService:
    def __init__(self, courts_repository: CourtsRepository = CourtsRepository()):
        self.courts_repository = courts_repository

    def get_all(self, query_params=None):
        courts = self.courts_repository.get_all(query_params)

        return to_courts_response(courts) if courts else []

