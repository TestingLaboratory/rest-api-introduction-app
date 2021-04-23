from fastapi import FastAPI
from rest_introduction_app.api.fundamentals import playing_with_headers, client_error, server_error, successful, \
    basic_authentication, serving_images, cookies, token_authentication

app = FastAPI(
    title='HTTP - REST API training',
    description="Token authentication training",
    version="0.1",
    docs_url="/",
    redoc_url=None
)

app.include_router(router=token_authentication.router,
                   tags=["Token Authentication"])
