"""
-- For Development Purposes --
Serves all all api challenges and training materials
Look out for auth clashes and multiple cookies
"""
from fastapi import FastAPI

from rest_introduction_app.api.api import api_router

app = FastAPI(
    title='Testing HTTP responses',
    description="Application to show different HTTP responses for learning testing purpose",
    version="0.1",
    docs_url="/",
    redoc_url=None
)

app.include_router(api_router, prefix='/api')
