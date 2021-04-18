#TODO move to basics
"""
Wheel of fortune

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
        "message": f"Welcome in Wheel of Fortune!. "
    }
