import json
from datetime import datetime, timedelta

from app.db.config import client


class CourtsRepository:
    def __init__(self):
        self.db_client = client
        # !TODO change the name of collection
        self.courts = self.db_client["tennis"]["courtsAvailability2"]

    def get_all(self, query_params=None):
        if not query_params:
            return self.courts.find()

        club_name = query_params.get("clubName")
        min_duration = query_params.get("minDuration")
        max_duration = query_params.get("maxDuration")
        days = query_params.get("days")
        is_league_slot = query_params.get("isLeagueSlot")

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

        if is_league_slot:
            query["isLeagueSlot"] = json.loads(is_league_slot)

        return self.courts.find(query)
