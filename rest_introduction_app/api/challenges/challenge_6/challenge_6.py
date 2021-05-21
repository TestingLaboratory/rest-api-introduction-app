# TODO challenge
"""
Diatlov Pass
- you need to pack your backback with utensils to get to te excursion to Diatlov Pass
- if you forget something you'll freeze to death
(restart endpoint needed!)
- you have to set up a tent and go to sleep to get your flag
"""
from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.params import Path
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from rest_introduction_app.api.challenges.challenge_6.model import Hiker, Item

challenge_tag = "Challenge - Excursions on Diatlov Pass"
router = APIRouter(prefix="/challenge/diatlov-pass")

hiker = Hiker()

# TODO add validation for pocket size items
# TODO fill in responses or delete them
item_responses = {
        "map": "Probably a good choice... not to follow the voices in your head.",
        "tent": "It is nice to have a piece of cloth over your head in the middle of nowhere...",
        "knife": "Keep it sharp. You never know what you might need it for.",
        "torch": "Shed some light on the unknown course of events.",
        "camera": "Take pictures and preserve moments for yourself... or others.",
        "lighter": "",
        "matches": "",
        "compass": "Follow the map to reach the northern Ural.",
        "thermos": "Ahhh... a sip of hot tea reminds of home, doesn't it?",
        "headlamp": "Go straight ahead, clear the path with a stream of light.",
        "bottled_water": "",
        "winter_jacket": "Hope you still own this jacket at the end of this journey :)",
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
    items = ",".join([item.name for item in hiker.backpack.content])
    return JSONResponse({
        "backpack_content": f"{items}"
    })


@router.get("/pocket_content", status_code=status.HTTP_200_OK)
async def pocket_content():
    items = ",".join([item.name for item in hiker.pocket.content])
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
                   f"Remember, all that matters is to survive."
    })


@router.patch("/swap_pocket_item/{item}", status_code=status.HTTP_201_CREATED)
async def swap_item(item_to_replace: Item,
                    item_to_pack: Item):
    hiker.pocket.swap_item(item_to_replace, item_to_pack)
    return JSONResponse({
        "message": f"You've decided to take {item_to_pack.name} instead of {item_to_replace.name}. "
                   f"Remember, all that matters is to survive."
    })


@router.put("/pack_all_to_backpack", status_code=status.HTTP_201_CREATED)
async def pack_all_to_backpack(items: List[Item] = Query(...)):
    hiker.backpack.put_items(items)
    return JSONResponse(
        {"message": "You've packed in a rush, huh? Do you have that strong feeling that you forgot something?"}
    )


@router.put("/pack_all_to_pocket", status_code=status.HTTP_201_CREATED)
async def pack_all_to_pocket(items: List[Item] = Query(...)):
    hiker.pocket.put_items(items)
    return JSONResponse(
        {"message": "You've packed in a rush, huh? Do you have that strong feeling that you forgot something?"}
    )


@router.delete("/remove_from_backapack", status_code=status.HTTP_200_OK)
async def remove_from_backpack(item: Item):
    hiker.backpack.remove_item(item)
    return JSONResponse(
        {"message": f"{item} has been removed from your backpack."}
    )


@router.delete("/remove_from_pocket", status_code=status.HTTP_200_OK)
async def remove_from_pocket(item: Item):
    hiker.pocket.remove_item(item)
    return JSONResponse(
        {"message": f"{item} has been removed from your pocket."}
    )
