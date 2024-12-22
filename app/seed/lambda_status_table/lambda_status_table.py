from app.db.config import client
from app.seed.consts import FetchingStatus


def run_lambda_status_table():
    tennis_db = client["tennis"]

    collection_name = "lambdaStatus"

    if collection_name in tennis_db.list_collection_names():
        return

    document = {"status": FetchingStatus.PREPARED, "lastUpdateStartTime": "", "lastUpdateEndTime": ""}
    lambda_status_table = client["tennis"]["lambdaStatus"]
    lambda_status_table.insert_one(document)
