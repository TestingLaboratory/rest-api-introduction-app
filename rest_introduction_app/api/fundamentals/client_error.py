import secrets

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status

from .core.responses import get_response

router = APIRouter()

security = HTTPBasic()


@router.get("/limited")
def get_limited_resource(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Username: Captain_snack, password: LateNightSausage
    """
    correct_username = secrets.compare_digest(credentials.username, "Captain_snack")
    correct_password = secrets.compare_digest(credentials.password, "LateNightSausage")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"The sausage is allowed for the {credentials.username}."
        )


@router.get("/things/{thing_id}")
def cant_find(thing_id: int):
    """
    Try to access a resource
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No resource with {thing_id=}"
    )


@router.post("/things/{thing_id}")
def unprocessable_entity(thing_id: int, body: dict):
    """
    Try to post anything here
    """
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"Oh nooo.... what did you did you?!"
    )


@router.put("/things/{thing_id}")
def unprocessable_entity(thing_id: int, body: dict):
    """
    Try to put anything here
    """
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"A-Team: there is BR instead of BA"
    )


@router.put("/server_operation/{operation_name}")
def unprocessable_entity(operation_name: str, body: dict):
    """
    Try to put anything here
    """
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"https://www.youtube.com/watch?v=nzlDYKR5otM"
    )