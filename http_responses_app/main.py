import uvicorn
from fastapi import FastAPI

from http_responses_app.api.api import api_router

app = FastAPI(
    title='Testing HTTP responses',
    description="Application to show different HTTP responses for learning testing purpose",
    version="0.1",
    docs_url="/",
    redoc_url=None
)

app.include_router(api_router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run(app=app,
                host="0.0.0.0",
                port=8000)
