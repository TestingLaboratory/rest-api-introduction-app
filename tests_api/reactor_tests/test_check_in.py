import random
import string

import requests

from tests_api.constants import BASE_URL, REACTOR_PATH, CHECK_IN_MESSAGE, FIELD_REQUIRED


def test_check_in(commander):
    payload = {"name": commander.name}
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
