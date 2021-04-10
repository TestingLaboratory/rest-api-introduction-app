#TODO challenge
# challenge for base 64, rot13, ascii to hex (uncover 3 flags using put/patch/post
# and try to uncover using /decode endpoint)
from fastapi import APIRouter
from starlette import status

router = APIRouter(prefix="/challenge/3")


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
