import uuid
from dataclasses import dataclass
from typing import List, Dict, Optional

from dataclasses_json import dataclass_json
from pydantic.main import BaseModel


@dataclass_json
@dataclass
class Resource:
    resource_type: str
    message: str
    amount: int
    linked_to: int
    locked: bool
    purged: bool

    def __init__(self, resource_type: str, message: str, amount: int = 1, linked_to: Optional[int] = None,
                 locked: bool = False, purged: bool = False):
        self.resource_type = resource_type
        self.message = message
        self.amount = amount
        self.linked_to = linked_to
        self.locked = locked
        self.purged = purged


class ResourcesCollection:
    def __init__(self):
        self.resources: Dict[User, List[Resource]] = {}


class UserRegistration(BaseModel):
    username: str
    password: str


@dataclass_json
class User:
    def __init__(self, username, password):
        self.username = username
        self.uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, username + password))
        self.methods_used = []

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __hash__(self):
        return hash((self.username, self.uuid))
