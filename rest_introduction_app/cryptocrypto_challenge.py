from fastapi import FastAPI

from rest_introduction_app.api.challenges.challenge_4 import challenge_4

app = FastAPI(
    title='Crypto-Cryptography',
    description="Crack the code, be a good Agent.",
    version="0.1",
    docs_url="/",
    redoc_url=None
)

app.include_router(router=challenge_4.router,
                   tags=[challenge_4.challenge_tag])
