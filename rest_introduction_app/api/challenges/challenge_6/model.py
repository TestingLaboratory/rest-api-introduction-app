import enum
from dataclasses import dataclass

from starlette.responses import JSONResponse


class Item(str, enum.Enum):
    tent = "tent"
    knife = "knife"
    torch = "torch"
    jacket = "jacket"
    matches = "matches"
    lighter = "lighter"
    compass = "compass"
    thermos = "thermos"
    headlamp = "headlamp"
    powerbank = "powerbank"
    smartphone = "smartphone"
    bottled_water = "bottled water"


@dataclass
class Storage:
    max_item_number: int
    content: list

    def __init__(self, max_item_number: int):
        self.max_item_number = max_item_number
        self.content = []

    def is_full(self):
        return len(self.content) >= self.max_item_number

    def add_item(self, item: Item):
        self.content.append(item)


@dataclass
class Hiker:
    backpack: Storage
    pocket: Storage

    def __init__(self):
        self.backpack = Storage(5)
        self.pocket = Storage(2)
