from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pydantic import BaseModel


class ChallengeSecret(BaseModel):
    secret: str


class PhoneCall(BaseModel):
    person: str
    phone_number: str
    subject: str


class Introduction(BaseModel):
    name: str


@dataclass_json
@dataclass
class Comrade:
    name: str
    uuid: str
