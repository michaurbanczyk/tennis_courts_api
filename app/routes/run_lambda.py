from fastapi import APIRouter

from app.models.run_lambda import RunLambda, RunLambdaStatus, RunLambdaStatusUpdate
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


@run_lambda_router.get("/status", response_model=RunLambdaStatus)
def get_run_lambda_status():

    run_lambda_service = RunLambdaService()
    run_status = run_lambda_service.get()

    return run_status


@run_lambda_router.patch("/update-status", response_model=RunLambdaStatus)
def update_run_lambda_status(body: RunLambdaStatusUpdate):

    run_lambda_service = RunLambdaService()
    run_status = run_lambda_service.update_run_lambda_status(**dict(body))

    return run_status
