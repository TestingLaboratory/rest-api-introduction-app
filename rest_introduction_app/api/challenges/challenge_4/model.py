import base64
import codecs
import uuid

import faker
from dataclasses_json import dataclass_json
from pydantic import BaseModel


class UserRegistration(BaseModel):
    username: str
    password: str


class HQMessage(BaseModel):
    message: str


FAKE = faker.Faker()


@dataclass_json
class User:
    def __init__(self, username, password):
        self.username = username
        self.uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, username + password))

    def __eq__(self, other):
        return self.uuid == other.uuid


def to_base64(text: str) -> str:
    text = base64.b64encode(bytes(text, 'utf-8'))
    return text.decode('utf-8')


def un_base64(text: str) -> str:
    text = base64.b64decode(text).decode('utf-8')
    return text


def rot13(text: str) -> str:
    return codecs.encode(text, 'rot_13')


def un_rot13(text: str) -> str:
    return codecs.decode(text, 'rot_13')


if __name__ == '__main__':
    flag = "${flag_agency_decryptor}"
    # flag = to_base64(flag)
    # print(flag)
    # flag = un_base64(flag)
    # print(flag)

    flag = to_base64(flag)
    print(flag)
    flag = to_base64(flag)
    print(flag)
    flag = rot13(flag)
    print(flag)
    flag = to_base64(flag)
    print(flag)
    flag = to_base64(flag)
    print(flag)
    flag = to_base64(flag)
    print(flag)
    flag = rot13(flag)
    print(flag)
    flag = to_base64(flag)
    print(flag)
    print("#" * 80)
    flag = un_base64(flag)
    print(flag)
    flag = un_rot13(flag)
    print(flag)
    flag = un_base64(flag)
    print(flag)
    flag = un_base64(flag)
    print(flag)
    flag = un_base64(flag)
    print(flag)
    flag = un_rot13(flag)
    print(flag)
    flag = un_base64(flag)
    print(flag)
    flag = un_base64(flag)
    print(flag)

tip = "UBURUBUBURUBUB"
