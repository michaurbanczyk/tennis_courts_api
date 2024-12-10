import json
from datetime import datetime, timedelta

from app.db.config import client


class AvailableCourtsRepository:
    def __init__(self):
        self.db_client = client
        self.courts_availability = self.db_client["tennis"]["courtsAvailability2"]

    def get_all(self, query_params=None):
        if not query_params:
            return self.courts_availability.find()

        club_name = query_params.get("clubName")
        min_duration = query_params.get("minDuration")
        max_duration = query_params.get("maxDuration")
        days = query_params.get("days")

        query = {}
        if club_name:
            query["clubName"] = {"$in": json.loads(club_name)}
        if min_duration or max_duration:
            query["duration"] = {}
            if min_duration:
                query["duration"]["$gte"] = int(json.loads(min_duration))
            if max_duration:
                query["duration"]["$lte"] = int(json.loads(max_duration))
        if days:
            num_of_days = [
                (datetime.now() + timedelta(days=day)).strftime("%Y/%m/%d")
                for day in range(0, int(json.loads(days)) + 1)
            ]
            query["date"] = {"$in": num_of_days}

        return self.courts_availability.find(query)
