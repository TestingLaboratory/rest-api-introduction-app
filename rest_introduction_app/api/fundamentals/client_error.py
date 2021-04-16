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
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The sausage is not allowed for the {credentials.username}."
        )
