from enum import Enum
from dataclasses import dataclass, field
from typing import List

from pydantic import BaseModel
from starlette.exceptions import HTTPException


class ItemName(Enum):
    map = "map"
    tent = "tent"
    knife = "knife"
    torch = "torch"
    camera = "camera"
    matches = "matches"
    lighter = "lighter"
    compass = "compass"
    thermos = "thermos"
    headlamp = "headlamp"
    bottled_water = "bottled water"
    winter_jacket = "winter jacket"


_POCKET_ITEM_NAMES = [ItemName.map, ItemName.knife, ItemName.torch,
                      ItemName.matches, ItemName.lighter, ItemName.compass]


class Item(BaseModel):
    name: ItemName


def is_pocket_size(item: Item):
    return item.name in _POCKET_ITEM_NAMES


class ReplaceItemModel(BaseModel):
    item_to_unpack: ItemName
    item_to_pack: ItemName


@dataclass
class Storage:
    storage_type: str
    max_item_number: int
    content: List = field(default_factory=lambda: [])


@dataclass
class Hiker:
    backpack: Storage = Storage("backpack", 5)
    pocket: Storage = Storage("pocket", 2)
    flags: List[str] = field(default_factory=lambda: [])

# Storage methods


def is_full(storage: Storage):
    return len(storage.content) >= storage.max_item_number


def add_item(storage: Storage, item: ItemName):
    storage.content.append(item)


def remove_item(storage: Storage, item: ItemName):
    if item in storage.content:
        storage.content.remove(item)
    else:
        raise HTTPException(status_code=400,
                            detail=f"Hmm, are you sure you've packed {item}?")


def put_items(storage: Storage, items: List[ItemName]):
    if len(items) <= storage.max_item_number:
        storage.content = items
    else:
        raise HTTPException(status_code=400,
                            detail=f"You can only pack {storage.max_item_number} items in your {storage.storage_type}")


def swap_item(storage: Storage, item_to_replace: ItemName, item_to_pack: ItemName):
    if item_to_replace in storage.content:
        itr_index = storage.content.index(item_to_replace)
        storage.content[itr_index] = item_to_pack
    else:
        raise HTTPException(status_code=400,
                            detail=f"Item '{item_to_replace}' not found in your inventory.")


# Hiker methods


def set_to_default(hiker: Hiker):
    hiker.backpack = Storage("backpack", 5)
    hiker.pocket = Storage("pocket", 2)


def get_backpack_content(hiker: Hiker):
    return ",".join([item.name for item in hiker.backpack.content])


def get_pocket_content(hiker: Hiker):
    return ",".join([item.name for item in hiker.pocket.content])


def is_item_packed(hiker: Hiker, item: ItemName):
    return item in hiker.backpack or item in hiker.pocket


def is_night_survived(hiker: Hiker, items_to_win):
    all_hiker_items = hiker.pocket.content + hiker.backpack.content
    return items_to_win in all_hiker_items


def missing_items_to_win(hiker: Hiker, items_to_win):
    all_hiker_items = hiker.pocket.content + hiker.backpack.content
    missing_items = [item for item in items_to_win if item not in all_hiker_items]
    return missing_items


    # def verify_flags(self):

#         iterate through items_to_win and add flags
