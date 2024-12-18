import json
from datetime import datetime, timedelta

from app.db.config import client


class CourtsRepository:
    def __init__(self):
        self.db_client = client
        self.courts = self.db_client["tennis"]["courts"]

    def get_all(self, query_params=None):
        if not query_params:
            return self.courts.find()

        club_name = query_params.get("clubName")
        min_duration = query_params.get("minDuration")
        max_duration = query_params.get("maxDuration")
        days = query_params.get("days")
        is_league_slot = query_params.get("isLeagueSlot")
        starts_from = query_params.get("startsFrom")
        ends_at = query_params.get("endsAt")

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

        if starts_from:
            query["startFloat"] = {"$gte": float(".".join(starts_from.split(":")))}

        if ends_at:
            query["endFloat"] = {"$lte": float(".".join(ends_at.split(":")))}

        return self.courts.find(query)
