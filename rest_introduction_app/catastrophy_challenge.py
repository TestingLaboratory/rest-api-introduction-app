from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from rest_introduction_app.api.challenges.challenge_1 import challenge_1

app = FastAPI(
    title="You're dealing with something that never occurred on this planet before",
    description="Find a way to us. in the face of first such event EVER!",
    version="0.1",
    docs_url="/",
    redoc_url=None
)

app.include_router(router=challenge_1.router,
                   tags=[challenge_1.challenge_tag])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
