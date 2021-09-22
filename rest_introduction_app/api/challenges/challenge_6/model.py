import enum
from dataclasses import dataclass, field
from typing import List

from pydantic import BaseModel
from starlette.exceptions import HTTPException

pocket_items = ["map", "knife", "torch", "matches", "lighter", "compass"]


class Item(str, enum.Enum):
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


class ItemModel(BaseModel):
    item: Item


class ReplaceItemModel(BaseModel):
    item_to_unpack: Item
    item_to_pack: Item

@dataclass
class Storage:
    storage_type: str
    max_item_number: int
    content: List = field(default_factory=lambda: [])

    def is_full(self):
        return len(self.content) >= self.max_item_number

    def add_item(self, item: Item):
        self.content.append(item)

    def remove_item(self, item: Item):
        if item in self.content:
            self.content.remove(item)
        else:
            raise HTTPException(status_code=400,
                                detail=f"Hmm, are you sure you've packed {item}?")

    def put_items(self, items: List[Item]):
        if len(items) <= self.max_item_number:
            self.content = items
        else:
            raise HTTPException(status_code=400,
                                detail=f"You can only pack {self.max_item_number} items in your {self.storage_type}")

    def swap_item(self, item_to_replace: Item, item_to_pack: Item):
        if item_to_replace in self.content:
            itr_index = self.content.index(item_to_replace)
            self.content[itr_index] = item_to_pack
        else:
            raise HTTPException(status_code=400,
                                detail=f"Item '{item_to_replace}' not found in your inventory.")

# TODO flags

@dataclass
class Hiker:
    # flags: list
    backpack: Storage = Storage("backpack", 5)
    pocket: Storage = Storage("pocket", 2)

    def set_to_default(self):
        self.backpack = Storage("backpack", 5)
        self.pocket = Storage("pocket", 2)

    def get_backpack_content(self):
        return ",".join([item.name for item in self.backpack.content])
