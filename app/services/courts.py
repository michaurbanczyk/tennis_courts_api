import json

from bson import ObjectId

from app.models.courts import to_courts_response
from app.repositories.courts import CourtsRepository


class CourtsService:
    def __init__(self, courts_repository: CourtsRepository = CourtsRepository()):
        self.courts_repository = courts_repository

    def get_all(self, query_params=None):

        courts = []
        if query_params:
            ids = query_params.get("ids")
            names = query_params.get("names")
            if ids:
                ids = json.loads(ids)
                object_ids = [ObjectId(id_) for id_ in ids]
                courts = self.courts_repository.get_by_id(object_ids)
            if names:
                names = json.loads(names)
                courts = self.courts_repository.get_by_name(names)
        else:
            courts = self.courts_repository.get_all()

        return to_courts_response(courts) if courts else []
