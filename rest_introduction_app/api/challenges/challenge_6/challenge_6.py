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
from text_unidecode import unidecode

from rest_introduction_app.api.challenges.challenge_6.model import Hiker, ItemName, Item, ReplaceItemModel, \
    _POCKET_ITEM_NAMES, set_to_default, get_backpack_content, is_full, add_item, is_pocket_size, put_items, remove_item, \
    get_pocket_content, swap_item, missing_items_to_win, HikerCheckIn

challenge_tag = "Challenge - Excursions on Diatlov Pass"
router = APIRouter(prefix="/challenge/diatlov-pass")

hikers = []

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
    "winter_jacket": "Hope you still own this jacket at the end of this journey :)"
}

ITEMS_TO_WIN = ["map", "tent", "knife", "torch", "lighter", "compass", "winter jacket"]

# TODO: fill in missing item responses
# TODO: ID as an endpoint path paramether
MISSING_ITEM_RESPONSES = {"map": "blabla",
                          "tent": "blabla",
                          "knife": "blabla",
                          "torch": "blabla",
                          "lighter": "blabla",
                          "compass": "blabla",
                          "winter jacket": "blabla"}


@router.get("/information", status_code=status.HTTP_200_OK)
async def information():
    return {
        "CRITICAL": "Development in progress. Sorry, this challenge is not ready yet."
    }


@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def check_in(hiker_check_in: HikerCheckIn):
    name = unidecode(hiker_check_in.name)
    if name not in [h.name for h in hikers]:
        hiker = Hiker(name)
        hikers.append(hiker)
        content = {
            "message": f"Take your badge and do not lose it. "
                       f"It allows you to pass through villages as a foreign. "
                       f"If anything happen, you'll be recognized by this ID card. "
                       "Удачи, товарищ.",
            "ID": f"{hiker.uuid}"
        }
        response = JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=content
        )
        return response
    else:

        return JSONResponse(
            status_code=422,
            content={
                "message": f"{hiker_check_in.name} has already registered. Do you want to go instead? "
                           f"I wouldn't recommend it. Believe me son..."
            }
        )


@router.get("/list_of_hikers", status_code=status.HTTP_200_OK)
async def participants():
    if hikers:
        return JSONResponse(
            content={
                "hikers": ", ".join([hiker.name for hiker in hikers])
            }
        )
    else:
        return JSONResponse(
            content={
                "message": "Currently no hiker has registered yet."
            }
        )


@router.get("{id_number}/sleep", status_code=status.HTTP_200_OK)
async def go_to_sleep(id_number: str):
    hiker = next(filter(lambda h: h.uuid == id_number, hikers), None)
    if hiker:
        missing_items = missing_items_to_win(hiker, ITEMS_TO_WIN)
        number_of_missing_items = len(missing_items)
        if number_of_missing_items == 0:
            return JSONResponse({
                "message": "Congratulations, brave scout! "
                           "You have been prepared for any unconventional types of danger! "
                           "You saved yourself with all of your excursion companions."
            })
        else:
            return JSONResponse({
                "message": MISSING_ITEM_RESPONSES[missing_items[0]]
            })
    else:
        return JSONResponse({
            "message": "Fake ID! A spy trying to sabotage the excursion! "
                       "Let the world forget about him forever, commander..."
        })


@router.get("{id_number}/restart", status_code=status.HTTP_200_OK)
async def restart(id_number: str):
    hiker = next(filter(lambda h: h.uuid == id_number, hikers), None)
    if hiker:
        set_to_default(hiker)
        return JSONResponse({
            "message": "Game has been restarted."
        })
    else:
        return JSONResponse({
            "message": "Fake ID! A spy trying to sabotage the excursion! "
                       "Let the world forget about him forever, commander..."
        })


@router.get("{id_number}/backpack_content", status_code=status.HTTP_200_OK)
async def backpack_content(id_number: str):
    hiker = next(filter(lambda h: h.uuid == id_number, hikers), None)
    if hiker:
        items = get_backpack_content(hiker)
        return JSONResponse({
            "backpack_content": f"{items}"
        })
    else:
        return JSONResponse({
            "message": "Fake ID! A spy trying to sabotage the excursion! "
                       "Let the world forget about him forever, commander..."
        })


@router.get("{id_number}/pocket_content", status_code=status.HTTP_200_OK)
async def pocket_content(id_number: str):
    hiker = next(filter(lambda h: h.uuid == id_number, hikers), None)
    if hiker:
        items = get_pocket_content(hiker)
        return JSONResponse({
            "pocket_content": f"{items}"
        })
    else:
        return JSONResponse({
            "message": "Fake ID! A spy trying to sabotage the excursion! "
                       "Let the world forget about him forever, commander..."
        })


@router.post("{id_number}/add_to_backpack")
async def add_to_backpack(id_number: str, body: Item):
    hiker = next(filter(lambda h: h.uuid == id_number, hikers), None)
    if hiker:
        if not is_full(hiker.backpack):
            add_item(hiker.backpack, body.name)
            return JSONResponse({
                "message": f"You've packed a {body.name.name}. {ITEM_RESPONSES.get(body.name.name)}."
            })
        else:
            raise HTTPException(status_code=400,
                                detail=f"Your backpack is full already.")
    else:
        return JSONResponse({
            "message": "Fake ID! A spy trying to sabotage the excursion! "
                       "Let the world forget about him forever, commander..."
        })


@router.post("{id_number}/add_to_pocket")
async def add_to_pocket(id_number: str, body: Item):
    hiker = next(filter(lambda h: h.uuid == id_number, hikers), None)
    if hiker:
        if not is_pocket_size(body):
            raise HTTPException(status_code=403,
                                detail=f"Are you trying to put {body.name.name} into your pocket? Really...")
        if is_full(hiker.pocket):
            raise HTTPException(status_code=400,
                                detail=f"Your pocket is full already.")
        add_item(hiker.pocket, body.name)
        return JSONResponse({
            "message": f"You've packed a {body.name.name}. {ITEM_RESPONSES.get(body.name.name)}"
        })
    else:
        return JSONResponse({
            "message": "Fake ID! A spy trying to sabotage the excursion! "
                       "Let the world forget about him forever, commander..."
        })


@router.patch("{id_number}/swap_backpack_item", status_code=status.HTTP_201_CREATED)
async def swap_backpack_item(id_number: str, body: ReplaceItemModel):
    hiker = next(filter(lambda h: h.uuid == id_number, hikers), None)
    if hiker:
        item_removed = body.item_to_unpack
        item_added = body.item_to_pack
        swap_item(hiker.backpack, item_removed, item_added)
        return JSONResponse({
            "message": f"You've decided to take {item_added.name} instead of {item_removed.name} "
                       f"Remember, all that matters is to survive."
        })
    else:
        return JSONResponse({
            "message": "Fake ID! A spy trying to sabotage the excursion! "
                       "Let the world forget about him forever, commander..."
        })


@router.patch("{id_number}/swap_pocket_item", status_code=status.HTTP_201_CREATED)
async def swap_pocket_item(id_number: str, body: ReplaceItemModel):
    hiker = next(filter(lambda h: h.uuid == id_number, hikers), None)
    if hiker:
        item_removed = body.item_to_unpack
        item_added = body.item_to_pack
        swap_item(hiker.pocket, item_removed, item_added)
        return JSONResponse({
            "message": f"You've decided to take {item_added.name} instead of {item_removed.name}. "
                       f"Remember, all that matters is to survive."
        })
    else:
        return JSONResponse({
            "message": "Fake ID! A spy trying to sabotage the excursion! "
                       "Let the world forget about him forever, commander..."
        })


@router.put("{id_number}/pack_all_to_backpack", status_code=status.HTTP_201_CREATED)
async def pack_all_to_backpack(id_number: str, items: List[ItemName] = Query(...)):
    hiker = next(filter(lambda h: h.uuid == id_number, hikers), None)
    if hiker:
        put_items(hiker.backpack, items)
        return JSONResponse(
            {"message": "You've packed in a rush, huh? Do you have that strong feeling that you forgot something?"}
        )
    else:
        return JSONResponse({
            "message": "Fake ID! A spy trying to sabotage the excursion! "
                       "Let the world forget about him forever, commander..."
        })


@router.put("{id_number}/pack_all_to_pocket", status_code=status.HTTP_201_CREATED)
async def pack_all_to_pocket(id_number: str, items: List[ItemName] = Query(...)):
    hiker = next(filter(lambda h: h.uuid == id_number, hikers), None)
    if hiker:
        if not all(itemName in _POCKET_ITEM_NAMES for itemName in items):
            raise HTTPException(status_code=403,
                                detail=f"Ugh agh... some of your items can't fit your pocket. Let's see...")
        put_items(hiker.pocket, items)
        return JSONResponse(
            {"message": "You've packed in a rush, huh? Do you have that strong feeling that you forgot something?"}
        )
    else:
        return JSONResponse({
            "message": "Fake ID! A spy trying to sabotage the excursion! "
                       "Let the world forget about him forever, commander..."
        })


@router.delete("{id_number}/remove_from_backpack", status_code=status.HTTP_200_OK)
async def remove_from_backpack(id_number: str, item: ItemName):
    hiker = next(filter(lambda h: h.uuid == id_number, hikers), None)
    if hiker:
        remove_item(hiker.backpack, item)
        return JSONResponse(
            {"message": f"{item} has been removed from your backpack."}
        )
    else:
        return JSONResponse({
            "message": "Fake ID! A spy trying to sabotage the excursion! "
                       "Let the world forget about him forever, commander..."
        })


@router.delete("{id_number}/remove_from_pocket", status_code=status.HTTP_200_OK)
async def remove_from_pocket(id_number: str, item: ItemName):
    hiker = next(filter(lambda h: h.uuid == id_number, hikers), None)
    if hiker:
        remove_item(hiker.pocket, item)
        return JSONResponse(
            {"message": f"{item} has been removed from your pocket."}
        )
    else:
        return JSONResponse({
            "message": "Fake ID! A spy trying to sabotage the excursion! "
                       "Let the world forget about him forever, commander..."
        })
