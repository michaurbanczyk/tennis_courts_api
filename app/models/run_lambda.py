from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class RunLambdaStatusEnum(StrEnum):
    STARTED = "Started"
    SUCCESS = "Success"
    ERROR = "Error"
    IN_PROGRESS = "In Progress"
    FINISHED = "Finished"
    PREPARED = "Prepared"


class RunLambda(BaseModel):
    info: str
    status: str


class RunLambdaStatus(BaseModel):
    status: str
    lastUpdateStartTime: str
    lastUpdateEndTime: str


class RunLambdaStatusUpdate(BaseModel):
    status: Optional[RunLambdaStatusEnum] = None
    lastUpdateStartTime: Optional[str] = None
    lastUpdateEndTime: Optional[str] = None


def to_run_lambda_status_response(run_lambda_response):
    return dict(run_lambda_response)
