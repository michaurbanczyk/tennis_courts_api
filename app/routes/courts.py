from fastapi import APIRouter

courts_router = APIRouter(
    prefix="/courts",
    tags=["courts"],
)


@courts_router.get("/")
async def hello_world():
    return {"response": "API is working!"}
