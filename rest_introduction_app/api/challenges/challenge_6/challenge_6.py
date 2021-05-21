# TODO challenge
"""
Diatlov Pass
- you need to pack your backback with utensils to get to te excursion to Diatlov Pass
- if you forget something you'll freeze to death
(restart endpoint needed!)
- you have to set up a tent and go to sleep to get your flag
"""
from fastapi import APIRouter, Depends
from fastapi.params import Path
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from rest_introduction_app.api.challenges.challenge_6.model import Hiker, Item

challenge_tag = "Challenge - Excursions on Diatlov Pass"
router = APIRouter(prefix="/challenge/diatlov-pass")
hiker = Hiker()


# TODO fill in responses or delete them
item_responses = {
        "tent": "It is nice to have a piece of cloth over your head in the middle of dark woods...",
        "knife": "Remember to sharpen it Comrade.",
        "torch": "",
        "jacket": "",
        "lighter": "",
        "compass": "",
        "thermos": "",
        "headlamp": "",
        "bottled_water": "",
        "food": []
    }


@router.get("/information", status_code=status.HTTP_200_OK)
async def information():
    return {
        "CRITICAL": "Development in progress. Sorry, this challenge is not ready yet."
    }


@router.get("/restart", status_code=status.HTTP_200_OK)
async def restart():
    hiker.set_to_default()
    return JSONResponse({
        "message": "Game has been restarted."
    })


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


@router.patch("/swap_backpack_item/{item}", status_code=status.HTTP_201_CREATED)
async def swap_item(item_to_replace: Item,
                    item_to_pack: Item):
    hiker.backpack.swap_item(item_to_replace, item_to_pack)
    return JSONResponse({
        "message": f"You've decided to take {item_to_pack.name} instead of {item_to_replace.name}. "
                   f"Remember, all that matters now is to survive."
    })


@router.patch("/swap_pocket_item/{item}", status_code=status.HTTP_201_CREATED)
async def swap_item(item_to_replace: Item,
                    item_to_pack: Item):
    hiker.pocket.swap_item(item_to_replace, item_to_pack)
    return JSONResponse({
        "message": f"You've decided to take {item_to_pack.name} instead of {item_to_replace.name}. "
                   f"Remember, all that matters now is to survive."
    })
