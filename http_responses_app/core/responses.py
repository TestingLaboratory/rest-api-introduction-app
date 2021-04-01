from datetime import datetime
from typing import Optional

from starlette.responses import JSONResponse

from http_responses_app.core.response_codes_information import get_code_information
from http_responses_app.model.pong import Pong


def get_response(status_code: int, additional_info: dict = None):
    return __response(status_code=status_code,
                      method="GET",
                      additional_info=additional_info)


def post_response(status_code: int, request_body: Pong):
    return __response(status_code,
                      method="POST",
                      request_body=request_body)


def put_response(status_code: int, request_body: Pong):
    return __response(status_code,
                      method="PUT",
                      request_body=request_body)


def __response(status_code: int, method: str,
               request_body: Optional[Pong] = None,
               additional_info: dict = None) -> JSONResponse:
    content = {"yourRequestBody": request_body.request_body} if request_body else {}

    if not additional_info:
        additional_info = {}

    additional_info.update(get_code_information(status_code))

    content.update({
        "basicInformation": f"This is {method} example for status code {status_code}",
        "responseInformation": additional_info,
        "timestamp": f"{datetime.now()}"})

    return JSONResponse(
        status_code=status_code,
        content=content
    )
