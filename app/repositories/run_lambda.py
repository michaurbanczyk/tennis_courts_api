from app.db.config import client


class RunLambdaRepository:
    def __init__(self):
        self.db_client = client
        self.run_lambda_status_collection = self.db_client["tennis"]["lambdaStatus"]

    def get(self):
        return self.run_lambda_status_collection.find_one()

    def update(self, update_query: dict):
        return self.run_lambda_status_collection.update_one({}, update_query)
