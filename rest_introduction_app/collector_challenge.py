from fastapi import FastAPI

from rest_introduction_app.api.challenges.challenge_5 import challenge_5

app = FastAPI(
    title='The METHOD-ical collector',
    description="Explore and catch them all",
    version="0.1",
    docs_url="/",
    redoc_url=None
)

app.include_router(router=challenge_5.router,
                   tags=[challenge_5.challenge_tag])
