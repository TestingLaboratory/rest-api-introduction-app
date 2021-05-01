# TODO challenge
"""
Diatlov Pass
- you need to pack your backback with utensils to get to te excursion to Diatlov Pass
- if you forget something you'll freeze to death
(restart endpoint needed!)
- you have to set up a tent and go to sleep to get your flag
"""
from fastapi import APIRouter, Depends
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from rest_introduction_app.api.challenges.challenge_6.model import Hiker, Item

challenge_tag = "Challenge - Excursions on Diatlov Pass"
router = APIRouter(prefix="/challenge/diatlov-pass")
hiker = Hiker()

#TODO try to add dependency to check if storage is full

# def check_capacity(storage: str):
#     storages = {"backpack": hiker.backpack.is_full(),
#                 "pocket": hiker.pocket.is_full()}
#     if storages.get(storage):
#         raise HTTPException(status_code=400,
#                             detail=f"Your {storage} is full already.")


# TODO fill in responses or delete them
item_responses = {
        "tent": "It is nice to have a piece of cloth over your head in the middle of dark woods...",
        "knife": "Remember to sharpen it MacGyver.",
        "torch": "",
        "jacket": "",
        "lighter": "",
        "compass": "",
        "thermos": "",
        "headlamp": "",
        "powerbank": "",
        "smartphone": "",
        "bottled_water": ""
    }


@router.get("/information", status_code=status.HTTP_200_OK)
async def information():
    return {
        "CRITICAL": "Development in progress. Sorry, this challenge is not ready yet."
    }


@router.get("/backpack_content", status_code=status.HTTP_200_OK)
async def backpack_content():
    items = [item.name for item in hiker.backpack.content]
    return JSONResponse({
        "backpack_content": f"{items}"
    })


@router.get("/pocket_content", status_code=status.HTTP_200_OK)
async def pocket_content():
    items = [item.name for item in hiker.pocket.content]
    return JSONResponse({
        "pocket_content": f"{items}"
    })


@router.post("/add_to_backpack/{item}")
async def add_to_backpack(item: Item):
    if not hiker.backpack.is_full():
        hiker.backpack.add_item(item)
        return JSONResponse({
            "message": f"You've packed a {item.name}. {item_responses.get(item.name)}."
        })
    else:
        raise HTTPException(status_code=400,
                            detail=f"Your backpack is full already.")

# TODO add validation for pocket size items
@router.post("/add_to_pocket/{item}")
async def add_to_pocket(item: Item):
    if not hiker.pocket.is_full():
        hiker.pocket.add_item(item)
        return JSONResponse({
            "message": f"You've packed a {item.name}. {item_responses.get(item.name)}."
        })
    else:
        raise HTTPException(status_code=400,
                            detail=f"Your pocket is full already.")
