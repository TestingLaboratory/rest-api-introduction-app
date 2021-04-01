from fastapi import APIRouter
from http_responses_app.api.endpoints import client_error, server_error, successful

api_router = APIRouter()

api_router.include_router(successful.router, tags=["Successful requests responses"])
api_router.include_router(client_error.router, tags=["Client error requests responses"])
api_router.include_router(server_error.router, tags=["Server error requests responses"])
