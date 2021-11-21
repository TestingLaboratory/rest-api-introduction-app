# TODO challenge
"""
Diatlov Pass
- you need to pack your backback with utensils to get to te excursion to Diatlov Pass
- if you forget something you'll freeze to death
(restart endpoint needed!)
- you have to set up a tent and go to sleep to get your flag
"""
from typing import List

from fastapi import APIRouter, Query
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from rest_introduction_app.api.challenges.challenge_6.model import Hiker, ItemName, Item, ReplaceItemModel, \
    _POCKET_ITEM_NAMES, set_to_default, get_backpack_content, is_full, add_item, is_pocket_size, put_items, remove_item

challenge_tag = "Challenge - Excursions on Diatlov Pass"
router = APIRouter(prefix="/challenge/diatlov-pass")
# router.include_router()

hiker = Hiker()

ITEM_RESPONSES = {
    "map": "Probably a good choice... not to follow the voices in your head.",
    "tent": "It is nice to have a piece of cloth over your head in the middle of nowhere...",
    "knife": "Keep it sharp. You never know what you might need it for.",
    "torch": "Shed some light on the unknown course of events.",
    "camera": "Take pictures and preserve moments for yourself... or others.",
    "lighter": "Light, fire, heat? A lighter gives you all of them.",
    "matches": "Starts up fast and goes out fast, like human destiny.",
    "compass": "Follow the map to reach the northern Ural.",
    "thermos": "Ahhh... a sip of hot tea reminds of home, doesn't it?",
    "headlamp": "Go straight ahead, clear the path with a stream of light.",
    "bottled_water": "Remember - plastic bottle can decompose for up to 1000 years." +
                     "That's much longer than the decomposition of the human body.",
    "winter_jacket": "Hope you still own this jacket at the end of this journey :)",
}

ITEMS_TO_WIN = ["map", "tent", "knife", "torch", "lighter", "compass", "winter jacket"]


@router.get("/information", status_code=status.HTTP_200_OK)
async def information():
    return {
        "CRITICAL": "Development in progress. Sorry, this challenge is not ready yet."
    }


@router.get("/restart", status_code=status.HTTP_200_OK)
async def restart():
    set_to_default(hiker)
    return JSONResponse({
        "message": "Game has been restarted."
    })


@router.get("/backpack_content", status_code=status.HTTP_200_OK)
async def backpack_content():
    items = get_backpack_content(hiker)
    return JSONResponse({
        "backpack_content": f"{items}"
    })


@router.get("/pocket_content", status_code=status.HTTP_200_OK)
async def pocket_content():
    items = ",".join([item.name for item in hiker.pocket.content])
    return JSONResponse({
        "pocket_content": f"{items}"
    })


@router.post("/add_to_backpack")
async def add_to_backpack(body: Item):
    if not is_full(hiker.backpack):
        add_item(hiker.backpack, body.name)
        return JSONResponse({
            "message": f"You've packed a {body.name.name}. {ITEM_RESPONSES.get(body.name.name)}."
        })
    else:
        raise HTTPException(status_code=400,
                            detail=f"Your backpack is full already.")


@router.post("/add_to_pocket")
async def add_to_pocket(body: Item):
    if not is_pocket_size(body):
        raise HTTPException(status_code=403,
                            detail=f"Are you trying to put {body.name.name} into your pocket? Really...")
    if is_full(hiker.pocket):
        raise HTTPException(status_code=400,
                            detail=f"Your pocket is full already.")
    add_item(hiker.pocket, body.name.name)
    return JSONResponse({
        "message": f"You've packed a {body.name.name}. {ITEM_RESPONSES.get(body.name.name)}."
    })


@router.patch("/swap_backpack_item", status_code=status.HTTP_201_CREATED)
async def swap_item(body: ReplaceItemModel):
    item_removed = body.item_to_unpack
    item_added = body.item_to_pack
    await swap_item(hiker.backpack, item_removed, item_added)
    return JSONResponse({
        "message": f"You've decided to take {item_added.name} instead of {item_removed.name}. "
                   f"Remember, all that matters is to survive."
    })


@router.patch("/swap_pocket_item", status_code=status.HTTP_201_CREATED)
async def swap_item(body: ReplaceItemModel):
    item_removed = body.item_to_unpack
    item_added = body.item_to_pack
    await swap_item(hiker.pocket, item_removed, item_added)
    return JSONResponse({
        "message": f"You've decided to take {item_added.name} instead of {item_removed.name}. "
                   f"Remember, all that matters is to survive."
    })


@router.put("/pack_all_to_backpack", status_code=status.HTTP_201_CREATED)
async def pack_all_to_backpack(items: List[ItemName] = Query(...)):
    put_items(hiker.backpack, items)
    return JSONResponse(
        {"message": "You've packed in a rush, huh? Do you have that strong feeling that you forgot something?"}
    )


@router.put("/pack_all_to_pocket", status_code=status.HTTP_201_CREATED)
async def pack_all_to_pocket(items: List[ItemName] = Query(...)):
    if not all(itemName in _POCKET_ITEM_NAMES for itemName in items):
        raise HTTPException(status_code=403,
                            detail=f"Ugh agh... some of your items can't fit your pocket. Let's see...")
    put_items(hiker.pocket, items)
    return JSONResponse(
        {"message": "You've packed in a rush, huh? Do you have that strong feeling that you forgot something?"}
    )


@router.delete("/remove_from_backpack", status_code=status.HTTP_200_OK)
async def remove_from_backpack(item: ItemName):
    remove_item(hiker.backpack, item)
    return JSONResponse(
        {"message": f"{item} has been removed from your backpack."}
    )


@router.delete("/remove_from_pocket", status_code=status.HTTP_200_OK)
async def remove_from_pocket(item: ItemName):
    remove_item(hiker.pocket, item)
    return JSONResponse(
        {"message": f"{item} has been removed from your pocket."}
    )
