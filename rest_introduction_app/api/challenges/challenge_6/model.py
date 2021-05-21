import enum
from dataclasses import dataclass
<<<<<<< HEAD
from typing import List

from pydantic import BaseModel
=======

>>>>>>> d89d654d25007b9ecd9a4bd324bc3e19c33eac12
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse


class Item(str, enum.Enum):
<<<<<<< HEAD
    map = "map"
    tent = "tent"
    knife = "knife"
    torch = "torch"
    camera = "camera"
=======
    tent = "tent"
    knife = "knife"
    torch = "torch"
    jacket = "jacket"
>>>>>>> d89d654d25007b9ecd9a4bd324bc3e19c33eac12
    matches = "matches"
    lighter = "lighter"
    compass = "compass"
    thermos = "thermos"
    headlamp = "headlamp"
<<<<<<< HEAD
    bottled_water = "bottled water"
    winter_jacket = "winter_jacket"
=======
    powerbank = "powerbank"
    smartphone = "smartphone"
    bottled_water = "bottled water"
>>>>>>> d89d654d25007b9ecd9a4bd324bc3e19c33eac12


@dataclass
class Storage:
<<<<<<< HEAD
    storage_type: str
    max_item_number: int
    content: list

    def __init__(self, storage_type: str, max_item_number: int):
        self.storage_type = storage_type
=======
    max_item_number: int
    content: list

    def __init__(self, max_item_number: int):
>>>>>>> d89d654d25007b9ecd9a4bd324bc3e19c33eac12
        self.max_item_number = max_item_number
        self.content = []

    def is_full(self):
        return len(self.content) >= self.max_item_number

    def add_item(self, item: Item):
        self.content.append(item)

<<<<<<< HEAD
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

=======
>>>>>>> d89d654d25007b9ecd9a4bd324bc3e19c33eac12
    def swap_item(self, item_to_replace, item_to_pack):
        if item_to_replace in self.content:
            itr_index = self.content.index(item_to_replace)
            self.content[itr_index] = item_to_pack
        else:
            raise HTTPException(status_code=400,
                                detail=f"Item '{item_to_replace}' not found in your inventory.")


@dataclass
class Hiker:
    backpack: Storage
    pocket: Storage

    def __init__(self):
<<<<<<< HEAD
        self.backpack = Storage("backpack", 5)
        self.pocket = Storage("pocket", 2)

    def set_to_default(self):
        self.backpack = Storage("backpack", 5)
        self.pocket = Storage("pocket", 2)

=======
        self.backpack = Storage(5)
        self.pocket = Storage(2)

    def set_to_default(self):
        self.backpack = Storage(5)
        self.pocket = Storage(2)
>>>>>>> d89d654d25007b9ecd9a4bd324bc3e19c33eac12
