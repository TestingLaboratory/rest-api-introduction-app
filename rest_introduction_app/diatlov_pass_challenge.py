from fastapi import FastAPI

from rest_introduction_app.api.challenges.challenge_6 import challenge_6

app = FastAPI(
    title='Excursion od Diatlov Pass',
    description="Prepare your backback, you're gonna need it!",
    version="0.1",
    docs_url="/",
    redoc_url=None
)

app.include_router(router=challenge_6.router,
                   tags=[challenge_6.challenge_tag])
