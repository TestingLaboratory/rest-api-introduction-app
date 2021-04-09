import secrets

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter()

security = HTTPBasic()


async def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "SeniorSiarra")
    correct_password = secrets.compare_digest(credentials.password, "JurekKiler")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A dzie mnie z tymi rencoma?!",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/users/me")
async def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username,
            "message": "You are logged in"}


@router.get("/users/some_secret_resource/{resource_id}")
async def read_current_user(resource_id: int, username: str = Depends(get_current_username)):
    return {"username": username,
            "message": f"Sztabka złota nr {resource_id} dla Ciebie!"}
