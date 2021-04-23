from fastapi import FastAPI

from rest_introduction_app.api.challenges.challenge_2 import challenge_2

app = FastAPI(
    title='RBMK Reactor test',
    description="What happens in reactor core - stays in reactor core. Or rather should have...",
    version="0.1",
    docs_url="/",
    redoc_url=None
)

app.include_router(router=challenge_2.router,
                   tags=[challenge_2.challenge_tag])
