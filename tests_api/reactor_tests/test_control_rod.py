import re

import requests

from tests_api.constants import BASE_URL, REACTOR_PATH, DELETE_CONTROL_ROD_MESSAGE, \
    PLACE_CONTROL_ROD_ALREADY_REMOVED_MESSAGE, PLACE_CONTROL_ROD_MESSAGE, DELETE_CONTROL_ROD_ALREADY_REMOVED
from tests_api.models.commander import Commander

commander = Commander()


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
