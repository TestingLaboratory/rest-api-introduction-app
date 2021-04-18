from fastapi import APIRouter

from rest_introduction_app.api.challenges.challenge_1 import challenge_1
from rest_introduction_app.api.challenges.challenge_2 import challenge_2
from rest_introduction_app.api.challenges.challenge_3 import challenge_3
from rest_introduction_app.api.challenges.challenge_4 import challenge_4
from rest_introduction_app.api.challenges.challenge_5 import challenge_5
from rest_introduction_app.api.challenges.challenge_primer import challenge_primer
from rest_introduction_app.api.fundamentals import playing_with_headers, client_error, server_error, successful, \
    basic_authentication, serving_images, cookies, token_authentication

api_router = APIRouter()

# api_router.include_router(router=successful.router,
#                           tags=["Successful requests responses"])
# api_router.include_router(router=client_error.router,
#                           tags=["Client error requests responses"])
# api_router.include_router(router=server_error.router,
#                           tags=["Server error requests responses"])
# api_router.include_router(router=playing_with_headers.router,
#                           tags=["Playing with headers responses"])
# api_router.include_router(router=basic_authentication.router,
#                           tags=["Basic auth example"])
# api_router.include_router(router=token_authentication.router,
#                           tags=["Token Authentication"])
# api_router.include_router(router=serving_images.router,
#                           tags=["Serving images"])
# api_router.include_router(router=cookies.router,
#                           tags=["Cookies"])
#
# api_router.include_router(router=challenge_primer.router,
#                           tags=["Challenge Primer - A warm-up for OUR testers!"])
# # api_router.include_router(router=challenge_1.router,
# #                           tags=[challenge_1.challenge_tag])
# api_router.include_router(router=challenge_2.router,
#                           tags=[challenge_2.challenge_tag])
# api_router.include_router(router=challenge_3.router,
#                           tags=[challenge_3.challenge_tag])
api_router.include_router(router=challenge_4.router,
                          tags=[challenge_4.challenge_tag])
# api_router.include_router(router=challenge_5.router,
#                           tags=[challenge_5.challenge_tag])
