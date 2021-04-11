# TODO challenge
# challenge for base 64, rot13, ascii to hex (uncover 3 flags using put/patch/post
# and try to uncover using /decode endpoint)
import uuid
from typing import Optional, List

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from starlette.responses import JSONResponse

from rest_introduction_app.api.challenges.challenge_4.model import UserRegistration, User

router = APIRouter(prefix="/challenge/4")
security = HTTPBasic()


@router.get("/information", status_code=status.HTTP_200_OK)
async def get_information():
    """
    Get this resource to obtain mission debrief
    """
    return {
        "message": f"You are an Agent in Bureau of People's Internet Network Deciphering Agency. "
                   f"You have received several messages that are currently stored in our system."
                   f"Use /message/{{id}} to retrieve message. "
                   f"Then use your knowledge and tools at your disposal (other endpoints) "
                   f"to decipher those messages. "
                   f"Hurry though, the timer is set to 2 hours. After that time the messages "
                   f"will be wiped out due to security reasons. "
                   f"Don't fail me. "
    }


AUTHORIZED: List[dict] = []
USERS: List[User] = []
AUTH_KEY = f"{uuid.uuid4()}_granted_to_see_restricted_documents_{uuid.uuid4()}"


def has_access(authorized_by: Optional[str] = Header(None)):
    if not authorized_by:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access Denied. Credentials missing!',
        )
    if not authorized_by == AUTH_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access Denied. ${flag_no_resource_for_ya}.',
        )


def has_credentials(credentials: HTTPBasicCredentials):
    user = User(credentials.username, credentials.password)
    if user not in USERS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        return True


@router.post("/register")
def register(user_registration: UserRegistration):
    user = User(user_registration.username, user_registration.password)
    if user in USERS:
        status_code = status.HTTP_400_BAD_REQUEST
        content = {"message": "You are already registered in the Agency!!!"}
    else:
        USERS.append(user)
        status_code = status.HTTP_201_CREATED
        content = {"message": f"User {user.username} successfully registered"}
    return JSONResponse(content=content, status_code=status_code)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        return JSONResponse(
            headers={"Authorized-by": f"{AUTH_KEY}"},
            content={"message": f"Welcome, {credentials.username}"}
        )


@router.put("/final_message", status_code=status.HTTP_202_ACCEPTED,
            dependencies=[Depends(has_access)])
async def final_message_post(credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        return JSONResponse(
            content=""  # todo FINISH
        )


@router.patch("/final_message", status_code=status.HTTP_202_ACCEPTED,
              dependencies=[Depends(has_access)])
async def final_message_post(credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        return JSONResponse(
            content=""  # todo FINISH
        )
