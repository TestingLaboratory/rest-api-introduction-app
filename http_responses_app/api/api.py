from fastapi import APIRouter

from http_responses_app.api.challenges.challenge_1 import challenge_1
from http_responses_app.api.challenges.challenge_2 import challenge_2
from http_responses_app.api.challenges.challenge_primer import challenge_primer
from http_responses_app.api.fundamentals import playing_with_headers, client_error, server_error, successful, \
    basic_authentication, serving_images, cookies

api_router = APIRouter()

api_router.include_router(router=successful.router,
                          tags=["Successful requests responses"])
api_router.include_router(router=client_error.router,
                          tags=["Client error requests responses"])
api_router.include_router(router=server_error.router,
                          tags=["Server error requests responses"])
api_router.include_router(router=playing_with_headers.router,
                          tags=["Playing with headers responses"])
api_router.include_router(router=basic_authentication.router,
                          tags=["Basic auth example"])
api_router.include_router(router=serving_images.router,
                          tags=["Serving images"])
api_router.include_router(router=cookies.router,
                          tags=["Cookies"])
api_router.include_router(router=challenge_primer.router,
                          tags=["Challenge Primer - A warm-up for OUR testers!"])
api_router.include_router(router=challenge_1.router,
                          tags=["Challenge 1 - You have dealing with something "
                                "that have never occurred on this planet before!"])
api_router.include_router(router=challenge_2.router,
                          tags=["Challenge 2 - RBMK Reactor usage"])
