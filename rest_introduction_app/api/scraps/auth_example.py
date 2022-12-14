"""create jwt with fastapi and jwt"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

import jwt
from dataclasses_json import dataclass_json
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "",
        "hashed_password": "$2b$12$vUAe24fzbRpVSDQc09HikO9n3xSrIkT2tVyW5DQMuA4yvyT7ohj6q",  # secret
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "",
        "hashed_password": "$2b$12$vUAe24fzbRpVSDQc09HikO9n3xSrIkT2tVyW5DQMuA4yvyT7ohj6q",  # secret
        "disabled": True,
    },
}

@dataclass
class UserInDB:
    username: str
    full_name: str
    email: str
    hashed_password: str
    disabled: bool


def get_user(username):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)


def verify_password(password, hashed_password):
    """
    check password with hashed password

    :param password:
    :param hashed_password:
    :return:
    """
    print(pwd_context.hash(secret=password))
    return pwd_context.verify(password, hashed_password)


def authenticate_user(username, password):
    """
    authenticate user
    :param username:
    :param password:
    :return:
    """
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@dataclass_json
@dataclass
class TokenData:
    sub: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    payload: TokenData = TokenData.from_dict(data)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    payload.iat = int(datetime.utcnow().timestamp())
    payload.exp = int(expire.timestamp())
    encoded_jwt = jwt.encode(payload.to_dict(), "secret", algorithm="HS256")
    return encoded_jwt



@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# access secret user data
@app.get("/users/me")
async def read_users_me(current_user: str = Depends(oauth2_scheme)):
    return {"username": current_user}

# access public user data
@app.get("/users/{username}")
async def read_user(username: str):
    user = get_user(username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

#register new user
@app.post("/users")
async def register_user(user: UserInDB):
    if user.username in fake_users_db:
        raise HTTPException(status_code=409, detail="User already registered")
    fake_users_db[user.username] = user
    return user


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=9011)
