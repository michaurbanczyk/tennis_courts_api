import json

from bson import ObjectId

from app.repositories.available_courts import AvailableCourtsRepository


class AvailableCourtsService:
    def __init__(self, available_courts_repository: AvailableCourtsRepository = AvailableCourtsRepository()):
        self.available_courts_repository = available_courts_repository

    def get_all(self, query_params=None):

        courts = []
        if query_params:
            ids = query_params.get("ids")
            names = query_params.get("names")
            if ids:
                ids = json.loads(ids)
                object_ids = [ObjectId(id_) for id_ in ids]
                courts = self.available_courts_repository.get_by_id(object_ids)
            if names:
                names = json.loads(names)
                courts = self.available_courts_repository.get_by_name(names)
        else:
            courts = self.available_courts_repository.get_all()

        return courts
