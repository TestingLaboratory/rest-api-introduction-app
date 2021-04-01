from fastapi import APIRouter
from http_responses_app.core.responses import get_response, post_response, put_response
from http_responses_app.model.pong import Pong

router = APIRouter()


@router.get("/ok")
async def get_response_200():
    return get_response(200)


@router.post("/created")
async def post_response_201(request: Pong):
    return post_response(201, request)


@router.put("/created")
async def put_response_201(request: Pong):
    return put_response(201, request)
