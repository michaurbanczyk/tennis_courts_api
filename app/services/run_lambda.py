import requests
from fastapi import HTTPException

from app.config import LAMBDA_RUN_ENDPOINT


class RunLambdaService:
    @staticmethod
    def run_lambda():

        response = requests.post(
            url=LAMBDA_RUN_ENDPOINT, headers={"X-Amz-Invocation-Type": "Event", "Content-Type": "application/json"}
        )

        if not response.ok:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return {"info": "success", "status": "200"}
