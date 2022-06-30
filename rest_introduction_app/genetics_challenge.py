import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9015)