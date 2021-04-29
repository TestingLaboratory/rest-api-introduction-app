# TODO challenge
"""
Diatlov Pass
- you need to pack your backback with utensils to get to te excursion to Diatlov Pass
- if you forget something you'll freeze to death
(restart endpoint needed!)
- you have to set up a tent and go to sleep to get your flag
"""
from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from rest_introduction_app.api.challenges.challenge_6.model import Hiker

challenge_tag = "Challenge - Excursions on Diatlov Pass"
router = APIRouter(prefix="/challenge/diatlov-pass")
hiker = Hiker()


@router.get("/information", status_code=status.HTTP_200_OK)
async def information():
    return {
        "CRITICAL": "Development in progress. Sorry, this challenge is not ready yet."
    }


@router.get("/backpack_content", status_code=status.HTTP_200_OK)
def backpack_content():
    return JSONResponse({
        "backpack_content": f"{hiker.backpack.content}"
    })


@router.get("/pocket_content", status_code=status.HTTP_200_OK)
def pocket_content():
    return JSONResponse({
        "pocket_content": f"{hiker.pocket.content}"
    })

# TODO walidacja itemów


@router.post("/add_to_backpack/{item}")
def add_to_backpack(item: str):
    hiker.backpack.content.append(item)


@router.post("/add_to_pocket/{item}")
def add_to_pocket(item: str):
    hiker.pocket.content.append(item)
