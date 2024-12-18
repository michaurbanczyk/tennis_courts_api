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
        ranges = self._get_ranges(query_params)

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

        if ranges:
            iter_ranges = iter(ranges)
            zipped = [(start, next(iter_ranges, "")) for start in iter_ranges]
            query["$or"] = [
                {
                    "$and": [
                        {"startFloat": {"$gte": float(".".join((z[0] if z[0] != "" else "00:00").split(":")))}},
                        {"endFloat": {"$lte": float(".".join((z[1] if z[1] != "" else "23:59").split(":")))}}
                    ]
                } for z in zipped
            ]

        return self.courts.find(query)

    @staticmethod
    def _get_ranges(query_params=None):
        query_params_keys = list(query_params.keys())
        return [query_params[key] for key in query_params_keys if "range" in key]
