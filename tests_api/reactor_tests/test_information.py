import random
import re
import string

import requests

from tests_api.constants import BASE_URL, REACTOR_PATH, INFORMATION_MESSAGE, CONTROL_ROOM_MESSAGE, \
    LOOK_INTO_REACTOR_CORE_MESSAGE, CURIOUS_FLAG, ANALYSIS_MESSAGE, CHECK_KEY_MESSAGE, KEY_ERROR_MESSAGE, \
    SNEAKY_RAT_FLAG


def test_get_information():
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/information")
    assert response.status_code == 200
    assert response.json()["message"] == INFORMATION_MESSAGE


def test_control_room(commander):
    commander.obtain_a_key()
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room")
    assert response.status_code == 200
    assert response.json()["reactor data"]
    assert re.fullmatch(CONTROL_ROOM_MESSAGE, response.json()["message"])


def test_control_room_key_error():
    random_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{random_key}/control_room")
    assert response.status_code == 403
    assert response.json()["message"] == f"{KEY_ERROR_MESSAGE} {SNEAKY_RAT_FLAG}"


def test_look_into_reactor_core(commander):
    commander.obtain_a_key()
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/reactor_core")
    assert response.status_code == 200
    assert re.fullmatch(LOOK_INTO_REACTOR_CORE_MESSAGE, response.json()["message"])
    assert re.fullmatch(CURIOUS_FLAG, response.json()["flag"])


def test_analysis(commander):
    commander.obtain_a_key()
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room/analysis")
    assert response.status_code == 200
    assert re.fullmatch(ANALYSIS_MESSAGE, response.json()["message"])


def test_check_key(commander):
    commander.obtain_a_key()
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/check_key/{commander.key}")
    assert response.status_code == 200
    assert response.json()["message"] == CHECK_KEY_MESSAGE
