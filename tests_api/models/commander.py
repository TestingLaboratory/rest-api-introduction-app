import requests
from faker import Faker


from tests_api.constants import BASE_URL, REACTOR_PATH


class Commander:
    def __init__(self, register_at_desk=True):
        self.faker = Faker()
        self.name = self.faker.name()
        if register_at_desk:
            self.key = self.obtain_a_key()

    def obtain_a_key(self):
        name = self.name
        payload = {"name": name}
        desk_response = requests.post(f"{BASE_URL}/{REACTOR_PATH}/desk", json=payload)
        assert desk_response.status_code == 201
        key = desk_response.json()["key"]
        return key
