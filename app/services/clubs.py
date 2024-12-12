import json

from bson import ObjectId

from app.models.clubs import to_clubs_response
from app.repositories.clubs import ClubsRepository


class ClubsService:
    def __init__(self, clubs_repository: ClubsRepository = ClubsRepository()):
        self.clubs_repository = clubs_repository

    def get_all(self, query_params=None):

        clubs = []
        if query_params:
            ids = query_params.get("ids")
            names = query_params.get("names")
            if ids:
                ids = json.loads(ids)
                object_ids = [ObjectId(id_) for id_ in ids]
                clubs = self.clubs_repository.get_by_id(object_ids)
            if names:
                names = json.loads(names)
                clubs = self.clubs_repository.get_by_name(names)
        else:
            clubs = self.clubs_repository.get_all()

        return to_clubs_response(clubs) if clubs else []
