import datetime
import uuid
from dataclasses import dataclass
from random import randint
from typing import List

import faker
from dataclasses_json import dataclass_json
from pydantic import BaseModel


class UserRegistration(BaseModel):
    username: str
    password: str

FAKE= faker.Faker()

@dataclass_json
class User:
    def __init__(self, username, password):
        self.username = username
        self.uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, username + password))
        self.final_message = next(word for word in (FAKE.word() for _ in range(10000)) if len(word) > 6)

    def __eq__(self, other):
        return self.uuid == other.uuid
