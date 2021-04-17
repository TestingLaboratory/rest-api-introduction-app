# TODO challenge
# challenge for base 64, rot13, ascii to hex (uncover 3 flags using put/patch/post
# and try to uncover using /decode endpoint)
import uuid
from typing import Optional, List

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from starlette.responses import JSONResponse

from rest_introduction_app.api.challenges.challenge_4.model import UserRegistration, User, to_base64, rot13, HQMessage, \
    un_rot13, un_base64
challenge_tag = "Challenge - Cryptography agency that just loooooooves acronyms."
router = APIRouter(prefix="/challenge/acronym_agency")
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
                   f"There are four flags waiting. "
                   f"Don't fail me. "
    }


AUTHORIZED: List[dict] = []
USERS: List[User] = []
AUTH_KEY = f"{uuid.uuid4()}_granted_to_see_restricted_documents_{uuid.uuid4()}"
MESSAGES = {}


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
        content = {"message": f"User {user.username} successfully registered"
                              f"User's unique identification number is: {user.uuid}"}
    return JSONResponse(content=content, status_code=status_code)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        return JSONResponse(
            headers={"Authorized-by": f"{AUTH_KEY}"},
            content={"message": f"Welcome, {credentials.username}"}
        )


@router.get("/encrypted_message", status_code=status.HTTP_202_ACCEPTED,
            dependencies=[Depends(has_access)])
async def encrypted_message(credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        user = User(credentials.username, credentials.password)
        if not MESSAGES.get(user.uuid):
            flag = f"${{flag_agency_decryptor_{user.uuid}}}"
            flag = to_base64(flag)
            flag = to_base64(flag)
            flag = rot13(flag)
            flag = to_base64(flag)
            flag = to_base64(flag)
            flag = to_base64(flag)
            flag = rot13(flag)
            flag = to_base64(flag)
            MESSAGES[user.uuid]["flag"] = flag
            message_for_hq = f"We serve the People's Internet Network Deciphering Agency"
            message_for_hq = to_base64(message_for_hq)
            message_for_hq = rot13(message_for_hq)
            message_for_hq = to_base64(message_for_hq)
            message_for_hq = to_base64(message_for_hq)
            message_for_hq = to_base64(message_for_hq)
            message_for_hq = rot13(message_for_hq)
            message_for_hq = rot13(message_for_hq)
            message_for_hq = rot13(message_for_hq)
            message_for_hq = to_base64(message_for_hq)
            message_for_hq = to_base64(message_for_hq)
            message_for_hq = to_base64(message_for_hq)
            MESSAGES[user.uuid]["secret"] = message_for_hq

            response = JSONResponse(
                content={
                    "message": MESSAGES.get(user.uuid).get("flag"),
                    "secret": f"POST {user.uuid}/headquarters with a decoded secret,"
                              f"but first GET the secret from the /box"
                }
            )
            response.set_cookie("message", "UBURUBUBURUBUB")
            response.set_cookie("secret", "UBUBUBURURURUBUBBURUB")
            return response


@router.get("/box", status_code=status.HTTP_200_OK,
            dependencies=[Depends(has_access)])
async def get_info_from_box(user_uuid: str, message_type: str,
                            credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        if secret := MESSAGES.get(user_uuid, {}).get(message_type):
            return JSONResponse(
                content={"envelope": secret}
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "The box looks empty..."}
            )


@router.post("{user_uuid}/headquarters", status_code=status.HTTP_202_ACCEPTED,
             dependencies=[Depends(has_access)])
async def final_message_post(user_uuid: str, hq_message: HQMessage,
                             credentials: HTTPBasicCredentials = Depends(security)):
    if has_credentials(credentials):
        content = {
            "message": f""
        }

        if hq_message.message == f"We serve the People's Internet Network Deciphering Agency":
            content["message"] = f"${{flag_you_know_how_acronyms_work_right?_{user_uuid}}}"
        else:
            content["message"] = f"${{not_yet_agent_{user_uuid}}}"

        return JSONResponse(
            content=content
        )


@router.get("{user_uuid}/crypto_engine", status_code=status.HTTP_200_OK,
            dependencies=[Depends(has_access), Depends(has_credentials)])
async def crypto_engine(user_uuid: str, method: str, message: str):
    methods = {
        "rot13": lambda text: rot13(text),
        "un_rot13": lambda text: un_rot13(text),
        "to_base64": lambda text: to_base64(text),
        "un_base64": lambda text: un_base64(text),

    }
    try:
        return JSONResponse(
            content=methods[method](message)
        )
    except (Exception or KeyError) as e:
        return JSONResponse(
            content={"message": "Wrong data to cipher or decipher",
                     "flag": f"${{flag_blind_testing_huh?_{user_uuid}}}"}
        )
