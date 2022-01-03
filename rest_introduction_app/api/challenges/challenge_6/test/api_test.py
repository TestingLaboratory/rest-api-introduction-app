import json

import pytest
from fastapi.testclient import TestClient

from rest_introduction_app.main import app

client = TestClient(app)
baseUrl = "/api/challenge/diatlov-pass"


@pytest.fixture()
def cleanup():
    yield
    path = "restart"
    client.get(f"{baseUrl}/{path}")


def test_valid_information():
    path = "information"
    response = client.get(f"{baseUrl}/{path}")
    json_data = json.loads(response.content)
    assert response.status_code == 200
    assert json_data == {"CRITICAL": "Development in progress. Sorry, this challenge is not ready yet."}


# TODO: check validation to False (is False) - not working!
def test_restart(cleanup):
    path = "restart"
    client.post(url=f"{baseUrl}/add_to_backpack",
                json={
                    "name": "tent"
                })
    client.post(url=f"{baseUrl}/add_to_pocket",
                json={
                    "name": "matches"
                })
    response = client.get(f"{baseUrl}/{path}")
    backpack_content = client.get(f"{baseUrl}/backpack_content")
    pocket_content = client.get(f"{baseUrl}/pocket_content")
    assert response.status_code == 200
    assert response.json()["message"] == "Game has been restarted."
    assert backpack_content.json()["backpack_content"] == ""
    assert pocket_content.json()["pocket_content"] == ""


@pytest.mark.parametrize("item", ["knife", "tent", "matches"])
def test_backpack_content(item, cleanup):
    client.put(url=f"{baseUrl}/pack_all_to_backpack?items={item}")
    path = "backpack_content"
    response = client.get(f"{baseUrl}/{path}")
    assert response.status_code == 200
    assert response.json()["backpack_content"] == f"{item}"


@pytest.mark.parametrize("item", ["compass", "knife", "matches"])
def test_pocket_content(item, cleanup):
    client.put(url=f"{baseUrl}/pack_all_to_pocket?items={item}")
    path = "pocket_content"
    response = client.get(f"{baseUrl}/{path}")
    assert response.status_code == 200
    assert response.json()["pocket_content"] == f"{item}"


def test_add_to_backpack(cleanup):
    path = "backpack_content"
    backpack_content_response = client.get(f"{baseUrl}/{path}")
    backpack_content_before_add = backpack_content_response.json()["backpack_content"].split(",")
    item_to_add = "tent"
    response = client.post(url=f"{baseUrl}/add_to_backpack",
                           json={
                               "name": item_to_add
                           })
    assert response.status_code == 200
    backpack_content_response = client.get(f"{baseUrl}/{path}")
    backpack_content_after_add = backpack_content_response.json()["backpack_content"].split(",")
    if backpack_content_before_add[0]:
        assert len(backpack_content_before_add) + 1 == len(backpack_content_after_add)
    else:
        assert len(backpack_content_after_add) == 1
    assert item_to_add in backpack_content_after_add


def test_add_to_pocket(cleanup):
    path = "pocket_content"
    pocket_content = client.get(f"{baseUrl}/{path}")
    pocket_content_before_add = pocket_content.json()["pocket_content"].split(",")
    item_to_add = "matches"
    response = client.post(url=f"{baseUrl}/add_to_pocket",
                           json={
                               "name": item_to_add
                           })
    assert response.status_code == 200
    pocket_content_response = client.get(f"{baseUrl}/{path}")
    pocket_content_after_add = pocket_content_response.json()["pocket_content"].split(",")
    if pocket_content_before_add[0]:
        assert len(pocket_content_before_add) + 1 == len(pocket_content_after_add)
    else:
        assert len(pocket_content_after_add) == 1
    assert item_to_add in pocket_content_after_add


def test_swap_item(cleanup):
    path = "swap_backpack_item"
    item_to_remove = "tent"
    item_to_add = "winter jacket"
    client.post(url=f"{baseUrl}/add_to_backpack",
                json={
                    "name": item_to_remove
                })
    response = client.patch(url=f"{baseUrl}/{path}",
                            json={
                                    "item_to_unpack": item_to_remove,
                                    "item_to_pack": item_to_add
                            })
    assert response.status_code == 201
