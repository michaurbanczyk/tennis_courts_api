from fastapi import APIRouter

from app.db.config import tennis_courts_collection
from app.models.courts import CourtResponse

courts_router = APIRouter(
    prefix="/courts",
    tags=["courts"],
)


@courts_router.get("/", response_model=CourtResponse)
async def courts():
    all_courts = []
    for court in tennis_courts_collection.find():
        all_courts.append({
            "id": str(court["_id"]),
            "name": court["name"],
            "freeSlots": court["courts"],
            "lastUpdated": court["last_updated"],
        })

    return {"courts": all_courts}
