import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from rest_introduction_app.api.fundamentals import playing_with_headers, client_error, server_error, successful, \
    basic_authentication, serving_images, cookies, token_authentication

app = FastAPI(
    title='HTTP - REST API training',
    description="HOW-TO and fiddle around basic Requests-Responses",
    version="0.1",
    docs_url="/",
    redoc_url=None
)

app.include_router(router=successful.router,
                   tags=["Successful requests responses"])
app.include_router(router=client_error.router,
                   tags=["Client error requests responses"])
app.include_router(router=server_error.router,
                   tags=["Server error requests responses"])
app.include_router(router=playing_with_headers.router,
                   tags=["Playing with headers responses"])
app.include_router(router=basic_authentication.router,
                   tags=["Basic auth example"])
app.include_router(router=serving_images.router,
                   tags=["Serving images"])
app.include_router(router=cookies.router,
                   tags=["Cookies"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9012)