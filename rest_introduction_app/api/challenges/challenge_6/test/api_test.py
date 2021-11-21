import json

import pytest
from fastapi.testclient import TestClient

from rest_introduction_app.main import app

client = TestClient(app)
baseUrl = "/api/challenge/diatlov-pass"


@pytest.fixture
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

