"""
This is the challenge primer to get testers to get accustomed with
the idea of CTF concept using REST API call
"""
import uuid

from dataclasses_json import dataclass_json
from fastapi import APIRouter
from pydantic.main import BaseModel
from starlette import status
from starlette.responses import JSONResponse, Response

router = APIRouter(prefix="/challenge/primer")
challenge_tag = "Challenge Primer - A warm-up for OUR testers!"


@router.get("/information", status_code=status.HTTP_200_OK)
async def get_information():
    """
    Get this resource to obtain mission debrief
    """
    return {
        "message": f"Oi! W'at can I do for ya? "
                   f"In this primer for challenges you'll learn how to look for flags. "
                   f"Remember that this is not purely technical task. "
                   f"You'll role play and use your knowledge to find treasures your looking for. "
                   f"If you have any questions - ask. "
                   f"Try and found as many flags as possible. (Five, there are five.) "
                   f"begin with shooting at /flag_info. "
    }


@router.get("/flag_info", status_code=status.HTTP_200_OK)
async def flag_info():
    """
    Fetch flags information
    """
    return {
        "flag": "A flag has a form of: ${<flag_name>}",
        "message": "Use your exploratory skills and feel the challenge's theme to obtain flags",
    }


@router.get("/flag/{flag_id}")
async def flag_info(flag_id: int):
    """
    Fetch flags information (there are two flags here ;) )
    """
    flags = {
        1: {"flag": "${flag_hello_there}", "status": status.HTTP_200_OK},
        6: {"flag": "${flag_general_kenobi}", "status": status.HTTP_200_OK}
    }
    data = flags.get(flag_id, {"flag": "Nope", "status": status.HTTP_404_NOT_FOUND})
    return JSONResponse(
        status_code=data["status"],
        content=data
    )


USERS = []


class UserRegistration(BaseModel):
    username: str
    password: str


@dataclass_json
class User:
    def __init__(self, username, password):
        self.username = username
        self.uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, username + password))

    def __eq__(self, other):
        return self.uuid == other.uuid


@router.post("/register")
def register(user_registration: UserRegistration):
    user = User(user_registration.username, user_registration.password)
    if user in USERS:
        status_code = status.HTTP_400_BAD_REQUEST
        content = {"message": "You are already registered in the Primer Challenge!",
                   "flag": "${flag_im_still_here_captain}"}
    else:
        USERS.append(user)
        status_code = status.HTTP_201_CREATED
        content = {"message": f"User {user.username} registered",
                   "key": f"{user.uuid}"}
    return JSONResponse(content=content, status_code=status_code)


@router.post("/login")
def login(user_registration: UserRegistration):
    user = User(user_registration.username, user_registration.password)
    cookie = None
    if user in USERS:
        content = {"message": f"Welcome, {user.username}, in the Primer!"}
        status_code = status.HTTP_202_ACCEPTED
        cookie = {"key": "session",
                  "value": f"${{flag_{user.uuid}_may_the_4th_b_with_u}}"}
    else:
        content = {"message": f"Failed to login. Wrong username or password.",
                   "flag": "${flag_naughty_aint_ya}"}
        status_code = status.HTTP_401_UNAUTHORIZED
    response = JSONResponse(content=content, status_code=status_code)
    if cookie:
        response.set_cookie(**cookie)
    return response
