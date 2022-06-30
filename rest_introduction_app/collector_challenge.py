from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from rest_introduction_app.api.challenges.challenge_5 import challenge_5

app = FastAPI(
    title='The METHOD-ical collector',
    description="Explore and catch them all",
    version="0.1",
    docs_url="/",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=challenge_5.router,
                   tags=[challenge_5.challenge_tag])
