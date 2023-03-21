import re

import requests

from tests_api.constants import BASE_URL, REACTOR_PATH, REMOVE_FUEL_ROD_MESSAGE, PUT_FUEL_ROD_MESSAGE
from tests_api.models.commander import Commander

commander = Commander()


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
