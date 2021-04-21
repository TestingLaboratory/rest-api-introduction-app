import uuid

from dataclasses_json import dataclass_json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic.main import BaseModel
from starlette import status
from starlette.requests import Request

router = APIRouter()


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


USERS = []


@router.get("/cookie_info")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies! "
                          "Use /register endpoint to obtain unique key"}
    return JSONResponse(content=content)


@router.post("/register")
def create_cookie(user_registration: UserRegistration):
    user = User(user_registration.username, user_registration.password)
    if user in USERS:
        status_code = status.HTTP_400_BAD_REQUEST
        content = {"message": "You are already registered to join the Empire!"}
    else:
        USERS.append(user)
        status_code = status.HTTP_201_CREATED
        content = {"message": f"User {user.username} registered",
                   "key": f"{user.uuid}"}
    return JSONResponse(content=content, status_code=status_code)


@router.post("/login")
def create_cookie(user_registration: UserRegistration):
    user = User(user_registration.username, user_registration.password)
    if user in USERS:
        content = {"message": f"Goooooood {user.username}, everything is proceeding just as I have foreseen it."}
        response = JSONResponse(content=content, status_code=status.HTTP_202_ACCEPTED)
        response.set_cookie(key="session", value=f"${user.uuid}_session_key")
    else:
        content = {"message": f"Failed to login. Wrong username or password."}
        response = JSONResponse(content=content, status_code=status.HTTP_401_UNAUTHORIZED)
    return response


@router.get("/for_logged_in_users_only")
def create_cookie(request: Request):
    try:
        session_key = request.cookies.get("session")
        user = list(filter(lambda u: u.uuid in session_key, USERS))[0]
        if user in USERS:
            content = {"message": f"Observe this fully operational battle station, young {user.username}."}
            response = JSONResponse(content=content, status_code=status.HTTP_200_OK)
        else:
            content = {"message": f"I find your lack of cookie disturbing..."}
            response = JSONResponse(content=content, status_code=status.HTTP_401_UNAUTHORIZED)
    except:
        content = {"message": f"I find your lack of cookie disturbing..."}
        response = JSONResponse(content=content, status_code=status.HTTP_401_UNAUTHORIZED)

    return response

