import requests
from faker import Faker


from tests_api.constants import BASE_URL, REACTOR_PATH


class Commander:
    faker = Faker()

    def __init__(self):
        self.name = Commander.faker.name()
        self.key = None

    def obtain_a_key(self):
        payload = {"name": self.name}
        desk_response = requests.post(f"{BASE_URL}/{REACTOR_PATH}/desk", json=payload)
        assert desk_response.status_code == 201
        key = desk_response.json()["key"]
        self.key = key
