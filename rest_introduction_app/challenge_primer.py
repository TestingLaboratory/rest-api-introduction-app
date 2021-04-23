from fastapi import FastAPI

from rest_introduction_app.api.challenges.challenge_primer import challenge_primer

app = FastAPI(
    title='Challenge primer',
    description="Application to show how Capture The Flag challenges work",
    version="0.1",
    docs_url="/",
    redoc_url=None
)

app.include_router(router=challenge_primer.router,
                   tags=[challenge_primer.challenge_tag])
