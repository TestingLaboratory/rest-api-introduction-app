"""
Missions for:
- Testing reactor
- Cleanup with robots/biorobots
- Boron, Sand, helicopters (random helicopter crashes into crane) 422Bad request if helicopter is overloaded
- Reactor building safety - percentages of Boron/Sand bags endpoint
"""
from collections import namedtuple

from fastapi import APIRouter, Request, status
from starlette.responses import JSONResponse
import uuid

from http_responses_app.api.challenges.authorization import AUTH_KEY, AUTH_KEY_VALUE, SECRET
from http_responses_app.api.challenges.challenge_1.model import ChallengeSecret, PhoneCall, Comrade, Introduction

router = APIRouter(prefix="/challenge/1")
Mission = namedtuple("mission", ["person", "phone_number", "subject"])  # task, resoultion?

comrades = []

chernobyl_mission = Mission("Anatolij Diatlov", "234-980-321", "The Test")
cleanup_mission = Mission("Boris Scherbina", "267-220-126", "The Cleanup")
western_robots_mission = Mission("Boris Yeltzin", "998-423-239", "The Joker")
bio_robots_mission = Mission("Valerij Legasov", "223-201-209", "The Bio Robots")


missions = [chernobyl_mission, cleanup_mission, western_robots_mission, bio_robots_mission]


@router.get("/first_steps", status_code=status.HTTP_200_OK)
async def how_to_authorize():
    """
    Get this resource to obtain instruction how to authorize
    within challenge_1 process
    """
    return {
        "message": f"You have to use 'secret' key with value {SECRET} in order to proceed. "
                   f"Use /authorize endpoint."
    }


@router.post("/authorize")
async def authorize(secret: ChallengeSecret):
    data = {}
    if secret.secret == SECRET:
        data.update(
            content={
                "message": "Greetings Comrade! In Soviet Russia the API calls you! "
                           "Use given information in headers to proceed:",
                AUTH_KEY: AUTH_KEY_VALUE}
        )
    else:
        data.update(
            status_code=401,
            content={
                "message": "Want to reach out for General Secretary secrets, Comrade? "
                           "Off to Gulag!!!"
            }
        )
    return JSONResponse(**data)


@router.post("/introduce_yourself")
async def introduce_yourself(introduction: Introduction, request: Request):
    if request.headers.get(AUTH_KEY) == AUTH_KEY_VALUE:
        comrade = Comrade(introduction.name,
                          str(uuid.uuid5(uuid.NAMESPACE_DNS, introduction.name)))
        comrades.append(comrade)
        return comrade
    else:
        return JSONResponse(
            status_code=401,
            content={
                "message": "I believe You're not from the Party, are you, Comrade?"
            }
        )


@router.get("/comrades")
async def get_all_comrades():
    return comrades


@router.get("/list_food")
async def authorize(request: Request):
    if request.headers.get(AUTH_KEY) == AUTH_KEY_VALUE:
        return JSONResponse(
            content={
                "message": "I propose a stakan of vodka and a piece of lard!",
                "mission": f"Make a phone call to >>{chernobyl_mission.person}<< about >>{chernobyl_mission.subject}<<.",
                "phone_number": f"{chernobyl_mission.phone_number}"
            }
        )
    else:
        return JSONResponse(
            status_code=401,
            content={
                "message": "I believe You're not from the Party, are you, Comrade?"
            }
        )


# TODO finish it
@router.post("/phone")
async def authorize(phone: PhoneCall, request: Request):
    data = {}

    if request.headers.get(AUTH_KEY) == AUTH_KEY_VALUE:
        data.update(
            content={
                "message": f"{phone.person} ",
                "mission": f"OI COMRADE!!!!. {phone.subject}",
                "phone_number": phone.phone_number
            }
        )
    else:
        data.update(
            status_code=401,
            content={
                "message": "I believe You're not from the Party, are you, Comrade?"
            }
        )
    return JSONResponse(**data)


# TODO finish it
@router.post("/phone/{phone_number}")
async def authorize(phone_number: str, phone_call: PhoneCall, request: Request):
    data = {}
    if request.headers.get(AUTH_KEY) == AUTH_KEY_VALUE:
        data.update(
            content={
                "message": "I propose a stakan of vodka and a piece of lard!",
                "mission": "Make a phone call to Anatolij Diatlov.",
                "phone_number": "234-980-321"
            }
        )
    else:
        data.update(
            status_code=401,
            content={
                "message": "I believe You're not from the Party, are you, Comrade?"
            }
        )
    return JSONResponse(**data)
