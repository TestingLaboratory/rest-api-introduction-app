"""
This is the challenge primer to get testers to get accustomed with
the idea of CTF concept using REST API call
"""
#TODO finish challenge primer for GET/POST/PUT
# and headers fiddling
# maybe introduce basic auth

from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter(prefix="/challenge/primer")


@router.get("/information", status_code=status.HTTP_200_OK)
async def get_information():
    """
    Get this resource to obtain mission debrief
    """
    return {
        "message": f"Oi! W'at can I do for ya?"
                   f"In this primer for challenges you'll learn how to look for flags."
                   f"Remember that this is not purely technical task"
                   f"You'll role play and use your knowledge to find treasures your looking for."
                   f"If you have any questions - ask."
                   f"Try and found as many flags as possible."
                   f"begin with shooting at /tryout."
    }


@router.get("/tryout", status_code=status.HTTP_200_OK)
async def tryout():
    """
    First steps in your CTF journey!
    """
    return {
        "message": f"Good! Toy have tried to GET a resource."
                   f"Now you have to GET something else... /flag"
    }


@router.get("/flag", status_code=status.HTTP_200_OK)
async def flag_info():
    """
    Fetch flags information
    """
    return {
        "flag": "A flag has a form of ${<flag_name>}",
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
        content=data["flag"]
    )
