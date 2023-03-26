import uvicorn
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from rest_introduction_app.api.challenges.challenge_2 import challenge_2

app = FastAPI(
    title='RBMK Reactor test',
    description="What happens in reactor core - stays in reactor core. Or rather should have...",
    version="0.1",
    docs_url="/",
    redoc_url=None,
)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as _:
        return JSONResponse({"message": "${nothing_to_see_here_move_along}"}, status_code=404)


app.add_exception_handler(404, catch_exceptions_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=challenge_2.router,
                   tags=[challenge_2.challenge_tag])


if __name__ == '__main__':
    uvicorn.run("__main__:app", host="0.0.0.0", port=9011, reload=True)
