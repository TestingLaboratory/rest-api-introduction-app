from datetime import datetime
from typing import Optional

from starlette.responses import JSONResponse

from http_responses_app.core.response_codes_information import get_code_information
from http_responses_app.model.pong import Pong


def get_response(status_code: int):
    return __response(status_code, "GET")


def post_response(status_code: int, request_body: Pong):
    return __response(status_code, "POST", request_body)


def put_response(status_code: int, request_body: Pong):
    return __response(status_code, "PUT", request_body)


def __response(status_code: int, method: str, request_body: Optional[Pong] = None) -> JSONResponse:
    content = {}
    if request_body is not None:
        content = {
            "yourRequestBody": request_body.request_body
        }
    content.update({
        "basicInformation": f"This is {method} example for status code {status_code}",
        "responseInformation": get_code_information(status_code),
        "timestamp": f"{datetime.now()}"})
    return JSONResponse(
        status_code=status_code,
        content=content
    )
