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
3. naughty - try to delete resource /1 - (it shouldn't be deleted and it acts as default to copy)
4. peek flag - use head on copied resource
5. link two resources together
6. unlink resource
7. lock resource
8. unlock resource
9. view.
10. options
11. purge
12 copy
13 copy linked resource (should copy both)
14. delete locked - shouldnt be deleted -
15. try to get nonexistent resource
"""
from typing import List, Dict
import json
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from rest_introduction_app.api.challenges.challenge_5.model import Resource, ResourcesCollection, UserRegistration, User

challenge_tag = "Challenge - The METHOD-ical Collector"
router = APIRouter(prefix="/challenge/methodical")


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
                   f"Remember to /register first"
                   f"P.S. DO NOT DELETE /resource with id = 1!"
    }


RESOURCES = ResourcesCollection()
security = HTTPBasic()


def has_credentials(credentials: HTTPBasicCredentials):
    user = User(credentials.username, credentials.password)
    if user not in RESOURCES.resources.keys():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        return user


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_registration: UserRegistration):
    user = User(user_registration.username, user_registration.password)
    if user in RESOURCES.resources.keys():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You are already registered for the hunt!!!")
    else:
        RESOURCES.resources.update({user: {1: Resource(resource_type="Golden",
                                                       message="Advised to not be meddled with!",
                                                       amount=1,
                                                       linked_to=None,
                                                       locked=False,
                                                       purged=False)
                                           }
                                    })
        return JSONResponse(content={"message": f"User {user.username} successfully registered"
                                                f"User's unique identification number is: {user.uuid}"})


@router.get("/resource/all", status_code=status.HTTP_200_OK)
async def get_resources(credentials: HTTPBasicCredentials = Depends(security)):
    if user := has_credentials(credentials):
        return JSONResponse(
            media_type="application/json",
            headers={"Explore": "Postman methods"},
            content={index: resource.__dict__ for index, resource in
                     RESOURCES.resources.get(user).items()}
        )


all_methods = {
    "GET": "",
    "POST": "",
    "PUT": "",
    "PATCH": "",
    "DELETE": "",
    "COPY": "",
    "HEAD": "",
    "OPTIONS": "",
    "LINK": "",
    "UNLINK": "",
    "PURGE": "",
    "LOCK": "",
    "UNLOCK": "",
    "PROPFIND": "",
    "VIEW": "",
}


# TODO finish this function
@router.api_route(path="/resource/{resource_id}", methods=list(all_methods.keys()), include_in_schema=False)
async def lock_resource(resource_id: int, request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    if user := has_credentials(credentials):
        try:
            if request.method == "GET":
                return RESOURCES.resources[user][resource_id]
            elif request.method == "POST":
                if resource_id in RESOURCES.resources[user].keys():
                    payload = await request.json()
                    RESOURCES.resources[user][resource_id] = Resource(**payload)
                else:
                    pass #TODO return already created
            elif request.method == "PUT":
                payload = await request.json()
                RESOURCES.resources[user][resource_id] = Resource(**payload)
            elif request.method == "PATCH":
                for name, value in request.body().__dict__:
                    RESOURCES.resources[user][resource_id].__setattr__(name, value)
            # resource = RESOURCES.resources.get(user)[resource_id]
            # result = method_actions.get(request.method)()
            # return result

        except KeyError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"${{flag_whatcha_gettin?_{user.uuid}}}")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{e=}")
