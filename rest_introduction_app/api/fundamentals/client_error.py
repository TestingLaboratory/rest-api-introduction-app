from fastapi import APIRouter
from http_responses_app.core.responses import get_response
router = APIRouter()

data = {}


@router.on_event("startup")
def startup_event():
    data["quota"] = 3
    data["limit"] = 0


@router.get("/limited")
async def get_response_403():
    data["limit"] += 1
    return get_response(200 if data["limit"] < data["quota"] else 403)
