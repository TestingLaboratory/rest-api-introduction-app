from fastapi import FastAPI

from rest_introduction_app.api.challenges.challenge_3 import challenge_3

app = FastAPI(
    title='Coronavirus anti-protein research',
    description="Humanity's last hope.",
    version="0.1",
    docs_url="/",
    redoc_url=None
)

app.include_router(router=challenge_3.router,
                   tags=[challenge_3.challenge_tag])
