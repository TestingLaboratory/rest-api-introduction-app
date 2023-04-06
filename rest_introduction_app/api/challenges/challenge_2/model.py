import uuid
from dataclasses import dataclass
from random import randint
from typing import List

from dataclasses_json import dataclass_json
from pydantic import BaseModel


class Purge(BaseModel):
    purge: bool = True


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
    def description(self):
        return self.__description

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
        if self.__state == "Unstable" and all(self.__control_rods):
            self.__state = "Operational"
        elif self.__state != "BOOM!!!":
            self.__calculate_state()
        return self.__state

    def __calculate_state(self):
        if self.__state not in ["Unstable", "Heavily Xenon-135 poisoned!"]:
            self.__state = "Operational"
        try:
            rods_ratio = len(list(filter(lambda x: x != "", self.__fuel_rods))) \
                         / len(list(filter(lambda x: x != "", self.__control_rods)))
            if rods_ratio > 15:
                self.__state = "Heavily Xenon-135 poisoned!"
            elif rods_ratio > 10 or (self.__power > 2000 and self.__state != "Heavily Xenon-135 poisoned!"):
                self.__state = "Unstable"
        except ZeroDivisionError:
            self.__state = "Critical! ${flag_safety_procedure_recklessly_omitted}"

    def remove_control_rod_at(self, index: int) -> str:
        try:
            if self.__control_rods[index] == "":
                return f"Control rod at {index} already removed!"
            self.__control_rods[index] = ""
            self.__calculate_state()
            if self.__state == "Operational":
                if self.__power == 0:
                    self.__power = randint(200, 250)
                self.__power += int(self.__power * 0.1)
            elif self.__state == "Unstable":
                self.__power += randint(50, 75)
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
            if self.__state in ["Operational", "Unstable"] and all(self.__control_rods):
                self.__power = 0
                self.__state = "Operational"
                return f"Adding control rod at {index}!"

            self.__calculate_state()
            power_to_subtract = 0
            if self.__state == "Operational":
                power_to_subtract = int(self.__power * 0.1)
            elif self.__state == "Unstable":
                power_to_subtract = randint(0, 200)
            if self.__state == "Heavily Xenon-135 poisoned!":
                self.__power += randint(300, 500)

            if self.__power - power_to_subtract <= 0:
                self.__power = 0
            else:
                self.__power -= power_to_subtract
            return f"Adding control rod at {index}!"
        except IndexError:
            return f"No such Control Rod with number >>{index}<<!"

    def press_az_5(self):
        self.__control_rods = list(map(lambda x: "control_rod", self.__control_rods))
        if self.__state in ["Heavily Xenon-135 poisoned!", "Critical! ${safety_procedure_recklessly_omitted}"] \
                and self.__power > 2000:
            self.__power = 30000
            self.__state = "BOOM!!!"
            self.__description = "${flag_for_reactor_due_to_3000%_work_norm}"
        else:
            self.__power = 0
        return self.__state

    def add_fuel_rod_at(self, index: int) -> str:
        try:
            if self.__fuel_rods[index] == "fuel_rod":
                return f"Fuel rod at {index} already in place!"
            self.__fuel_rods[index] = "fuel_rod"
            if all(self.__control_rods):
                return "Reactor is shut down... Remove some of the control rods first!"
            self.__calculate_state()
            if self.__state == "Operational":
                self.__power += int(self.__power * 0.05)  # originally 20
            elif self.__state == "Unstable":
                self.__power += randint(50, 100)
            if self.__state == "Heavily Xenon-135 poisoned!":
                self.__power += randint(5, 10)
            return f"Adding fuel rod at {index}!"
        except IndexError:
            return f"No such Fuel Rod with number >>{index}<<!"

    def remove_fuel_rod_at(self, index: int) -> str:
        try:
            if self.__fuel_rods[index] == "":
                return f"Fuel rod at {index} already in out!"
            self.__fuel_rods[index] = ""
            # fix issue with negative power - power should never be negative
            self.__calculate_state()
            power_to_subtract = 0
            if self.__state == "Operational":
                power_to_subtract = int(self.__power * 0.05)  # orginally 20
            elif self.__state == "Unstable":
                power_to_subtract = randint(0, 10)
            elif self.__state == "Heavily Xenon-135 poisoned!":
                self.__power += randint(300, 500)

            if self.__power <= power_to_subtract:
                self.__power = 0
            else:
                self.__power -= power_to_subtract
            return f"Removing fuel rod at {index}!"
        except IndexError:
            return f"No such Fuel Rod with number >>{index}<<!"
