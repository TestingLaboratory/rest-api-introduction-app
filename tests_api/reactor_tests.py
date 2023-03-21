import random
import re
import string

import requests

from tests_api.constants import *
from tests_api.models.commander import Commander

commander = Commander()


def test_get_information():
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/information")
    assert response.status_code == 200
    assert response.json()["message"] == INFORMATION_MESSAGE


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


def test_control_room():
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room")
    assert response.status_code == 200
    assert response.json()["reactor data"]
    assert re.search(CONTROL_ROOM_MESSAGE, response.json()["message"])


def test_control_room_key_error():
    random_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{random_key}/control_room")
    assert response.status_code == 403
    assert response.json()["message"] == f"{KEY_ERROR_MESSAGE} {SNEAKY_RAT_FLAG}"


def test_delete_control_rod():
    control_room_response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room")
    used_rod_index = list(control_room_response.json()["reactor data"]["_ReactorCore__control_rods"]).index(
        "control_rod")
    response = requests.delete(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room/control_rods/{used_rod_index}")
    assert response.status_code == 202
    assert re.search(DELETE_CONTROL_ROD_MESSAGE, response.json()["message"])


def test_delete_control_rod_already_removed():
    control_room_response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room")
    empty_rod_index = list(control_room_response.json()["reactor data"]["_ReactorCore__control_rods"]).index("")
    response = requests.delete(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room/control_rods/{empty_rod_index}")
    assert response.status_code == 202
    assert re.search(PLACE_CONTROL_ROD_ALREADY_REMOVED_MESSAGE, response.json()["message"])


def test_place_control_rod():
    control_room_response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room")
    empty_rod_index = list(control_room_response.json()["reactor data"]["_ReactorCore__control_rods"]).index("")
    response = requests.put(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room/control_rods/{empty_rod_index}")
    assert response.status_code == 200
    assert re.search(PLACE_CONTROL_ROD_MESSAGE, response.json()["message"])


def test_place_control_rod_already_in_place():
    control_room_response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room")
    used_rod_index = list(control_room_response.json()["reactor data"]["_ReactorCore__control_rods"]).index(
        "control_rod")
    response = requests.put(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room/control_rods/{used_rod_index}")
    assert response.status_code == 200
    assert re.search(DELETE_CONTROL_ROD_ALREADY_REMOVED, response.json()["message"])


def test_manipulate_az_5():
    payload = {"pressed": True}
    response = requests.put(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room/az_5", json=payload)
    assert response.status_code == 425
    assert re.search(MANIPULATE_AZ_5_MESSAGE, response.json()["message"])
    assert re.search(CHERENKOV_CHICKEN_FLAG, response.json()["flag"])


def test_unpress_az_5():
    payload = {"pressed": False}
    response = requests.put(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room/az_5", json=payload)
    assert response.status_code == 400
    assert response.json()["message"] == UNPRESS_AZ_5_MESSAGE


def test_look_into_reactor_core():
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/reactor_core")
    assert response.status_code == 200
    assert re.search(LOOK_INTO_REACTOR_CORE_MESSAGE, response.json()["message"])
    assert re.search(CURIOUS_FLAG, response.json()["flag"])


def test_analysis():
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room/analysis")
    assert response.status_code == 200
    assert re.search(ANALYSIS_MESSAGE, response.json()["message"])


def test_remove_fuel_rod():
    control_room_response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room")
    fuel_rod_index = list(control_room_response.json()["reactor data"]["_ReactorCore__fuel_rods"]).index("fuel_rod")
    response = requests.delete(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room/fuel_rods/{fuel_rod_index}")
    assert response.status_code == 202
    assert re.search(REMOVE_FUEL_ROD_MESSAGE, response.json()["message"])


def test_put_fuel_rod():
    control_room_response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room")
    empty_rod_index = list(control_room_response.json()["reactor data"]["_ReactorCore__fuel_rods"]).index("")
    response = requests.put(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/control_room/fuel_rods/{empty_rod_index}")
    assert response.status_code == 200
    assert re.search(PUT_FUEL_ROD_MESSAGE, response.json()["message"])


def test_reset_progress():
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/reset_progress")
    assert response.status_code == 200
    assert response.json()["message"] == RESET_PROGRESS_MESSAGE
    assert response.json()["flag"] == DIDNT_SEE_THE_GRAPHITE_FLAG


def test_check_key():
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/check_key/{commander.key}")
    assert response.status_code == 200
    assert response.json()["message"] == CHECK_KEY_MESSAGE
