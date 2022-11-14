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
        self.control_rod_manipulation = 0
        self.fuel_rod_manipulation = 0


@dataclass_json
class ReactorCore:
    __NOMINAL_POWER: int = 1000

    def __init__(self, uuid):
        __max_fuel_rods = 100  # originally in RBMK Reactor 1661
        __max_control_rods = 20  # originally in RBMK Reactor 211
        self.__uuid = uuid
        self.__power: int = randint(300, 500)
        self.__fuel_rods: List[str] = ["fuel_rod" for _ in range(__max_fuel_rods)]
        self.__control_rods: List[str] = ["control_rod" for _ in range(__max_control_rods)]
        # initial control rods removal
        for _ in range(randint(__max_control_rods // 4, __max_control_rods // 2)):
            self.__control_rods[randint(0, __max_control_rods - 1)] = ""
        # initial fuel rods removal
        for _ in range(randint(__max_fuel_rods // 5, __max_fuel_rods // 3)):
            self.__fuel_rods[randint(0, __max_fuel_rods - 1)] = ""
        self.__state = 'Operational'
        self.__description = "Rieaktor Bolszoj Moszcznosti Kanalnyj - 1000 MW"

    def __eq__(self, other):
        return self.__uuid == other.uuid

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

    #TODO improve calculations to blow up the reactor only when AZ5 is used
    def __calculate_state(self):
        try:
            rods_ratio = len(list(filter(lambda x: x != "", self.__fuel_rods))) \
                         / len(list(filter(lambda x: x != "", self.__control_rods)))
            if rods_ratio < 10:
                self.__state = "Operational"
            elif rods_ratio < 20:
                self.__state = "Unstable"
            elif rods_ratio < 40:
                self.__state = "Heavily Xenon-135 poisoned!"
            else:
                self.__state = "BOOM!!!"
                self.__power = 30_000
                self.__description = "${flag_for_reactor_due_to_3000%_work_norm}"
        except ZeroDivisionError:
            self.__state = "BOOM!!!"
            self.__power = 30_000
            self.__description = "${flag_for_reactor_due_to_3000%_work_norm}"

    def remove_control_rod_at(self, index: int) -> str:
        try:
            if self.__control_rods[index] == "":
                return f"Control rod at {index} already removed!"
            self.__control_rods[index] = ""
            self.__calculate_state()
            if self.__state == "Operational":
                self.__power += 75
            elif self.__state == "Unstable":
                self.__power += randint(0, 100)
            if self.__state == "Heavily Xenon-135 poisoned!":
                self.__power += randint(300, 500)
            return f"Removing control rod at {index}!"
        except IndexError:
            return f"No such Control Rod with number >>{index}<<!"

    def add_control_rod_at(self, index: int) -> str:
        try:
            if self.__control_rods[index] == "control_rod":
                return f"Control rod at {index} already in place!"
            self.__control_rods[index] = "control_rod"
            self.__calculate_state()
            if self.__state == "Operational":
                self.__power -= 30
            elif self.__state == "Unstable":
                self.__power -= randint(0, 50)
            if self.__state == "Heavily Xenon-135 poisoned!":
                self.__power += randint(300, 500)
            return f"Adding control rod at {index}!"
        except IndexError:
            return f"No such Control Rod with number >>{index}<<!"

    def press_az_5(self):
        self.__control_rods = list(map(lambda x: "control_rod", self.__control_rods))
        if self.__state == "Heavily Xenon-135 poisoned!" \
                and self.__power > 1500:
            self.__power = 30000
            self.__state = "BOOM!!!"
            self.__description = "${flag_for_reactor_due_to_3000%_work_norm}"
        return self.__state

    def add_fuel_rod_at(self, index: int) -> str:
        try:
            if self.__fuel_rods[index] == "fuel_rod":
                return f"Fuel rod at {index} already in place!"
            self.__fuel_rods[index] = "fuel_rod"
            self.__calculate_state()
            if self.__state == "Operational":
                self.__power += randint(50, 100)
            elif self.__state == "Unstable":
                self.__power += randint(0, 100)
            if self.__state == "Heavily Xenon-135 poisoned!":
                self.__power += randint(300, 500)
            return f"Adding fuel rod at {index}!"
        except IndexError:
            return f"No such Fuel Rod with number >>{index}<<!"

    def remove_fuel_rod_at(self, index: int) -> str:
        try:
            if self.__fuel_rods[index] == "":
                return f"Fuel rod at {index} already in out!"
            self.__fuel_rods[index] = ""
            self.__calculate_state()
            if self.__state == "Operational":
                self.__power -= 20
            elif self.__state == "Unstable":
                self.__power -= randint(0, 20)
            if self.__state == "Heavily Xenon-135 poisoned!":
                self.__power += randint(300, 500)
            return f"Removing fuel rod at {index}!"
        except IndexError:
            return f"No such Fuel Rod with number >>{index}<<!"
