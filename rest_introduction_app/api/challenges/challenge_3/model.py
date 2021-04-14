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
        self.uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, name))
        self.nucleocreator = 0
        self.aminoacid_appender = 0
        self.mutator = 0
        self.reductor = 0
        self.eradicator = 0
        self.architect = 0
        self.observer = 0
        self.achievements = {"nucleocreator": self.nucleocreator >= 10,
                             "aminoacid_appender": self.aminoacid_appender >= 10,
                             "mutator": self.mutator >= 10,
                             "reductor": self.reductor >= 10,
                             "eradicator": self.eradicator >= 10,
                             "architect": self.architect >= 50,
                             "observer": self.observer >= 5}
