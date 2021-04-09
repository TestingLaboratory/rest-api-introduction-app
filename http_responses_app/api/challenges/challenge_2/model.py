import uuid
from dataclasses import dataclass
from random import randint
from typing import List

from dataclasses_json import dataclass_json
from pydantic import BaseModel


class CommanderCheckIn(BaseModel):
    name: str


class AZ5(BaseModel):
    pressed: bool


@dataclass_json
@dataclass
class Commander:
    name: str
    uuid: str

    def __init__(self, name):
        self.name = name
        self.uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, name))


@dataclass_json
class ReactorCore:
    #TODO add flag for fuel rods and power
    __NOMINAL_POWER: int = 1000

    def __init__(self, uuid):
        self.__uuid = uuid
        self.__power: int = randint(300, 500)
        self.__fuel_rods: List[str] = ["fuel_rod" for _ in range(1661)]
        self.__control_rods: List[str] = ["control_rod" for _ in range(211)]
        # initial control rods removal
        for _ in range(randint(20, 50)):
            self.__control_rods[randint(0, 210)] = ""
        # initial fuel rods removal #TODO check how well it plays
        for _ in range(randint(300, 600)):
            self.__fuel_rods[randint(0, 1660)] = ""
        self.__state = 'Operational'

    @property
    def uuid(self):
        return self.__uuid

    @property
    def power(self):
        return self.__power

    @property
    def fuel_rods(self):
        return self.__fuel_rods

    @property
    def control_rods(self):
        return self.__control_rods

    @property
    def state(self):
        self.__calculate_state()
        return self.__state

    def __calculate_state(self):
        try:
            rods_ratio = len(self.__fuel_rods) / len(list(filter(lambda x: x != "", self.__control_rods)))
            # print(rods_ratio)
            if rods_ratio < 100:
                self.__state = "Operational"
            elif rods_ratio < 200:
                self.__state = "Unstable"
            elif rods_ratio < 400:
                self.__state = "Heavily Xenon-135 poisoned!"
            else:
                self.__state = "BOOM!!!"
                self.__power = 30_000
        except ZeroDivisionError:
            self.__state = "BOOM!!!"
            self.__power = 30_000

    def remove_control_rod_at(self, index: int) -> str:
        try:
            if self.__control_rods[index] == "":
                return f"Control rod at {index} already removed!"
            self.__control_rods[index] = ""
            if self.__state == "Operational":
                self.__power += 1
            elif self.__state == "Unstable":
                self.__power += randint(0, 1)
            if self.__state == "Heavily Xenon-135 poisoned!":
                self.__power += randint(300, 500)
            return f"Removing control rod at {index}!"
        except IndexError:
            return f"No such Control Rod with number >>{index}<<!"

    def add_control_rod_at(self, index: int) -> str:
        try:
            self.__control_rods[index] = "control_rod"
            return f"Adding control rod at {index}!"
        except IndexError:
            return f"Control Rod number >>{index}<< already in place!"

    def press_az_5(self):
        self.__control_rods = map(lambda x: "control_rod", self.__control_rods)
        if self.__state == "Heavily Xenon-135 poisoned!" \
                and self.__power > 1500:
            self.__power = 30000
            self.__state = "BOOM!!!"
        return self.__state


    #TODO add fuctionality of fuel rods insertions

if __name__ == '__main__':
    commander = Commander("Sasha")
    print(commander)
    core = ReactorCore(commander.uuid)
    # print(core.power)
    # print(core.fuel_rods)
    # print(core.control_rods)
    # print(core.state)
    for index in range(211):
        core.remove_control_rod_at(index)
        print(core.power)
        print(core.state)
