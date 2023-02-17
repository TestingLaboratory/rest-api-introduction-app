import re

import requests
from faker import Faker

from tests_api.constants import *

FAKE = Faker()


def test_get_information():
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/information")
    assert response.status_code == 200
    assert response.json()["message"] == INFORMATION_MESSAGE


def test_check_in():
    fake_name = FAKE.name()
    payload = {"name": fake_name}
    response = requests.post(f"{BASE_URL}/{REACTOR_PATH}/desk", json=payload)
    assert response.status_code == 201
    assert response.json()["key"]
    assert response.json()["message"] == CHECK_IN_MESSAGE


def test_control_room(obtain_a_key):
    fake_name = FAKE.name()
    key = obtain_a_key(fake_name)
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{key}/control_room")
    assert response.status_code == 200
    assert response.json()["reactor data"]
    assert re.search(CONTROL_ROOM_MESSAGE, response.json()["message"])


def test_delete_control_rod(obtain_a_key):
    fake_name = FAKE.name()
    key = obtain_a_key(fake_name)
    control_room_response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{key}/control_room")
    used_rod_index = list(control_room_response.json()["reactor data"]["_ReactorCore__control_rods"]).index(
        "control_rod")
    response = requests.delete(f"{BASE_URL}/{REACTOR_PATH}/{key}/control_room/control_rods/{used_rod_index}")
    assert response.status_code == 202
    assert re.search(DELETE_CONTROL_ROD_MESSAGE, response.json()["message"])


def test_place_control_rod(obtain_a_key):
    fake_name = FAKE.name()
    key = obtain_a_key(fake_name)
    control_room_response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{key}/control_room")
    empty_rod_index = list(control_room_response.json()["reactor data"]["_ReactorCore__control_rods"]).index("")
    response = requests.put(f"{BASE_URL}/{REACTOR_PATH}/{key}/control_room/control_rods/{empty_rod_index}")
    assert response.status_code == 200
    assert re.search(PLACE_CONTROL_ROD_MESSAGE, response.json()["message"])


def test_manipulate_az_5(obtain_a_key):
    fake_name = FAKE.name()
    key = obtain_a_key(fake_name)
    payload = {"pressed": True}
    response = requests.put(f"{BASE_URL}/{REACTOR_PATH}/{key}/control_room/az_5", json=payload)
    assert response.status_code == 425
    assert re.search(MANIPULATE_AZ_5_MESSAGE, response.json()["message"])
    assert re.search(CHERENKOV_CHICKEN_FLAG, response.json()["flag"])


def test_look_into_reactor_core(obtain_a_key):
    fake_name = FAKE.name()
    key = obtain_a_key(fake_name)
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{key}/reactor_core")
    assert response.status_code == 200
    assert re.search(LOOK_INTO_REACTOR_CORE_MESSAGE, response.json()["message"])
    assert re.search(CURIOUS_FLAG, response.json()["flag"])


def test_analysis(obtain_a_key):
    fake_name = FAKE.name()
    key = obtain_a_key(fake_name)
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{key}/control_room/analysis")
    assert response.status_code == 200
    assert re.search(ANALYSIS_MESSAGE, response.json()["message"])


def test_remove_fuel_rod(obtain_a_key):
    fake_name = FAKE.name()
    key = obtain_a_key(fake_name)
    control_room_response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{key}/control_room")
    fuel_rod_index = list(control_room_response.json()["reactor data"]["_ReactorCore__fuel_rods"]).index("fuel_rod")
    response = requests.delete(f"{BASE_URL}/{REACTOR_PATH}/{key}/control_room/fuel_rods/{fuel_rod_index}")
    assert response.status_code == 202
    assert re.search(REMOVE_FUEL_ROD_MESSAGE, response.json()["message"])


def test_put_fuel_rod(obtain_a_key):
    fake_name = FAKE.name()
    key = obtain_a_key(fake_name)
    control_room_response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{key}/control_room")
    empty_rod_index = list(control_room_response.json()["reactor data"]["_ReactorCore__fuel_rods"]).index("")
    response = requests.put(f"{BASE_URL}/{REACTOR_PATH}/{key}/control_room/fuel_rods/{empty_rod_index}")
    assert response.status_code == 200
    assert re.search(PUT_FUEL_ROD_MESSAGE, response.json()["message"])


def test_reset_progress(obtain_a_key):
    fake_name = FAKE.name()
    key = obtain_a_key(fake_name)
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{key}/reset_progress")
    assert response.status_code == 200
    assert response.json()["message"] == RESET_PROGRESS_MESSAGE
    assert response.json()["flag"] == DIDNT_SEE_THE_GRAPHITE_FLAG


def test_check_key(obtain_a_key):
    fake_name = FAKE.name()
    key = obtain_a_key(fake_name)
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/check_key/{key}")
    assert response.status_code == 200
    assert response.json()["message"] == CHECK_KEY_MESSAGE
