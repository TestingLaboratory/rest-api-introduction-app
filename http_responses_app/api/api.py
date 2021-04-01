from fastapi import APIRouter
from http_responses_app.api.endpoints import playing_with_headers, client_error, server_error, successful

api_router = APIRouter()

api_router.include_router(router=successful.router,
                          tags=["Successful requests responses"])
api_router.include_router(router=client_error.router,
                          tags=["Client error requests responses"])
api_router.include_router(router=server_error.router,
                          tags=["Server error requests responses"])
api_router.include_router(router=playing_with_headers.router,
                          tags=["Playing with headers responses"])
