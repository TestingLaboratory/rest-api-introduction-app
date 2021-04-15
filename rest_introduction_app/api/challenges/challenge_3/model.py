import uuid
from dataclasses import dataclass

from dataclasses_json import dataclass_json
from pydantic import BaseModel


class TechnicianCheckIn(BaseModel):
    username: str
    password: str


@dataclass_json
@dataclass
class LabTechnician:
    name: str
    password: str

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, name + password))
        self.nucleocreator = 100
        self.aminoacid_appender = 100
        self.mutator = 100
        self.reductor = 100
        self.eradicator = 100
        self.architect = 100
        self.observer = 100
        self.proteomaster = False
        self.achievements = {"nucleocreator": False,
                             "aminoacid_appender": False,
                             "mutator": False,
                             "reductor": False,
                             "eradicator": False,
                             "architect": False,
                             "observer": False}

    def calculate_achievements(self):
        self.achievements["nucleocreator"] = self.nucleocreator >= 10
        self.achievements["aminoacid_appender"] = self.aminoacid_appender >= 10
        self.achievements["mutator"] = self.mutator >= 10
        self.achievements["reductor"] = self.reductor >= 10
        self.achievements["eradicator"] = self.eradicator >= 10
        self.achievements["architect"] = self.architect >= 50
        self.achievements["observer"] = self.observer >= 5

    def translation_completed(self):
        self.proteomaster = True
