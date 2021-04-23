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

challenge_tag = "Challenge - Excursions on Diatlov Pass"
router = APIRouter(prefix="/challenge/diatlov-pass")


@router.get("/information", status_code=status.HTTP_200_OK)
async def information():
    return {
        "CRITICAL": "Development in progress. Sorry, this challenge is not ready yet."
    }
