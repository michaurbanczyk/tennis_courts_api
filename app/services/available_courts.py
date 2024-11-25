import json
from datetime import datetime, timedelta

from bson import ObjectId

from app.models.available_courts import to_available_courts_response
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

        return to_available_courts_response(courts) if courts else []

    def get_all_by_dates(self, query_params=None):
        courts = self.get_all(query_params)
        # in the future it might be configurable via query param
        num_of_days = 30
        days = [datetime.now() + timedelta(days=day) for day in range(0, num_of_days)]
        courts_by_dates = {day.strftime("%Y/%m/%d"): [] for day in days}
        for club in courts:
            club_name = club["name"]
            courts = club["courts"]
            for court in courts:
                free_slots = court["freeSlots"]
                court_name = court["name"]
                if free_slots:
                    for slot in free_slots:
                        date = slot["date"]
                        total_free_slots = slot["totalFreeSlots"]
                        for tfs in total_free_slots:
                            if date in courts_by_dates.keys():
                                courts_by_dates[date].append({**tfs, "name": club_name, "courtName": court_name})

        return courts_by_dates
