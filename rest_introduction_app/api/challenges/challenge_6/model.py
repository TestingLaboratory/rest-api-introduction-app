from dataclasses import dataclass

from starlette.responses import JSONResponse


@dataclass
class Storage:
    max_item_number: int
    content: list

    def __init__(self, max_item_number: int):
        self.max_item_number = max_item_number
        self.content = []


@dataclass
class Hiker:
    backpack: Storage
    pocket: Storage

    def __init__(self):
        self.backpack = Storage(7)
        self.pocket = Storage(3)
