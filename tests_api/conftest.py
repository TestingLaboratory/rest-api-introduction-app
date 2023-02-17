import pytest
import requests

from tests_api.constants import BASE_URL, REACTOR_PATH


@pytest.fixture
def obtain_a_key():
    def _obtain_a_key(name):
        fake_name = name
        payload = {"name": fake_name}
        desk_response = requests.post(f"{BASE_URL}/{REACTOR_PATH}/desk", json=payload)
        assert desk_response.status_code == 201
        key = desk_response.json()["key"]
        return key

    return _obtain_a_key
