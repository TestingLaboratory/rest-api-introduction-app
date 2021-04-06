from fastapi import APIRouter, Request

from http_responses_app.core.responses import get_response

router = APIRouter()

auth_dict = {
    "apikey": "woohoo"
}

non_authorized = {
    "whoopsie": "Probably you should ask for the auth key"
}


@router.get("/header_check")
async def check_your_request_header(request: Request):
    """
    Try that on Swagger Docs. If should return status code 200.
    """

    return get_response(200 if request.headers.get("apikey") == auth_dict.get("apikey") else 403, non_authorized)

