import random
import string

import requests

from tests_api.constants import BASE_URL, REACTOR_PATH, CHECK_IN_MESSAGE, FIELD_REQUIRED
from tests_api.models.commander import Commander


def test_check_in():
    commander_not_registered = Commander(register_at_desk=False)
    payload = {"name": commander_not_registered.name}
    response = requests.post(f"{BASE_URL}/{REACTOR_PATH}/desk", json=payload)
    assert response.status_code == 201
    assert response.json()["key"]
    assert response.json()["message"] == CHECK_IN_MESSAGE


def test_check_in_validation_error():
    random_value = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    error_payload = {"error_field": random_value}
    response = requests.post(f"{BASE_URL}/{REACTOR_PATH}/desk", json=error_payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == FIELD_REQUIRED
