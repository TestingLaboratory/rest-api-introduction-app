# TODO challenge
"""
The Collector
Create User, use basic auth and then
use following methods:
GET/POST/PUT/PATCH/DELETE/COPY/HEAD/OPTIONS/LINK/UNLINK/PURGE/LOCK/UNLOCK/VIEW

to gather flags write test cases with logical flow
following flags:
1. explore flag - use all methods at least once
2. eraser flag - delete one of created data with id >2
3. naughty - try to delete recource /1 - (it shouldn't be deleted and it acts as default to copy)
4. peek flag - use head on copied resource
5. link two resources together
6. unink resource
7. lock resource
8. unlock resource
9. view.
10. options
11. purge
12 copy
13 copy linked resource (should copy both)
14. delete locked - shouldnt be deleted -
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
