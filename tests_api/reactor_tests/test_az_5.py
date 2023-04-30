import re

import requests

from tests_api.constants import BASE_URL, REACTOR_PATH, MANIPULATE_AZ_5_MESSAGE, CHERENKOV_CHICKEN_FLAG, \
    UNPRESS_AZ_5_MESSAGE


def test_manipulate_az_5(commander):
    commander.obtain_a_key()
    payload = {"pressed": True}
    response = requests.put(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room/az_5", json=payload)
    assert response.status_code == 425
    assert re.fullmatch(MANIPULATE_AZ_5_MESSAGE, response.json()["message"])
    assert re.fullmatch(CHERENKOV_CHICKEN_FLAG, response.json()["flag"])


def test_unpress_az_5(commander):
    commander.obtain_a_key()
    payload = {"pressed": False}
    response = requests.put(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room/az_5", json=payload)
    assert response.status_code == 400
    assert response.json()["message"] == UNPRESS_AZ_5_MESSAGE
