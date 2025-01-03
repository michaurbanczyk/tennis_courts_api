from datetime import datetime, timedelta

import requests
from fastapi import HTTPException

from app.config import (
    DATETIME_FORMAT,
    LAMBDA_RUN_ENDPOINT,
    LAMBDA_RUN_INTERVAL,
    timezone,
)
from app.models.run_lambda import to_run_lambda_status_response
from app.repositories.run_lambda import RunLambdaRepository


class RunLambdaService:
    def __init__(self, run_lambda_repository: RunLambdaRepository = RunLambdaRepository()):
        self.run_lambda_repository = run_lambda_repository

    def run_lambda(self):
        run_lambda_status = self.run_lambda_repository.get()

        current_time = datetime.now(timezone)
        last_update_start_time = datetime.strptime(run_lambda_status.get("lastUpdateStartTime"), DATETIME_FORMAT)

        two_hours_delta = last_update_start_time + timedelta(hours=int(LAMBDA_RUN_INTERVAL))
        if current_time < two_hours_delta:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Last update has been run at: {last_update_start_time.strftime('%H:%M:%S')}."
                    f" {LAMBDA_RUN_INTERVAL} hours have to passed to be able to run it again."
                ),
            )

        print("SENDING REQUEST!")
        response = requests.post(
            url=LAMBDA_RUN_ENDPOINT, headers={"X-Amz-Invocation-Type": "Event", "Content-Type": "application/json"}
        )

        if not response.ok:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return {"info": "success", "status": "200"}

    def get(self):
        run_lambda_status = self.run_lambda_repository.get()

        return to_run_lambda_status_response(run_lambda_status) if run_lambda_status else {}

    def update_run_lambda_status(self, **kwargs):

        current_lambda_status = self.run_lambda_repository.get()
        if not current_lambda_status:
            raise HTTPException(status_code=404, detail="Item not found")

        self.run_lambda_repository.update({
            "$set": {
                "status": kwargs.get("status") if kwargs.get("status") else current_lambda_status["status"],
                "lastUpdateStartTime": (
                    kwargs.get("lastUpdateStartTime")
                    if kwargs["lastUpdateStartTime"]
                    else current_lambda_status["lastUpdateStartTime"]
                ),
                "lastUpdateEndTime": (
                    kwargs.get("lastUpdateEndTime")
                    if kwargs.get("lastUpdateEndTime")
                    else current_lambda_status["lastUpdateEndTime"]
                ),
            },
        })

        updated_lambda_status = self.run_lambda_repository.get()

        return to_run_lambda_status_response(updated_lambda_status if updated_lambda_status else current_lambda_status)
