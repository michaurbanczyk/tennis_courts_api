from fastapi import APIRouter

from app.models.run_lambda import RunLambda
from app.services.run_lambda import RunLambdaService

run_lambda_router = APIRouter(
    prefix="/run-lambda",
    tags=["run-lambda"],
)


@run_lambda_router.post("/", response_model=RunLambda)
def run_lambda():

    run_lambda_service = RunLambdaService()
    run_status = run_lambda_service.run_lambda()

    return run_status
