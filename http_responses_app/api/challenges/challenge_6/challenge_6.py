#TODO challenge
"""


"""
from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter(prefix="/challenge/5")


@router.get("/information", status_code=status.HTTP_200_OK)
async def get_information():
    """
    Get this resource to obtain mission debrief
    """
    return {
        "message": f"Welcome Collector. "
                   f"Your purpose is collect. Have them all."
                   f"And have them all logically. "
                   f"Use every method at your fingertips to create logical flows "
                   f"and retrieve as many flags as possible."
                   f"Make us proud! And remember to show off your collection!"
                   f"PS. DO NOT delete resource with id = 1!"
    }
