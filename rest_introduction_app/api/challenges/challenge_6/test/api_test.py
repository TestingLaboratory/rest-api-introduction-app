import json

from fastapi.testclient import TestClient
from rest_introduction_app.main import app

client = TestClient(app)
prefix = "/api/challenge/diatlov-pass"


def test_valid_information():
    response = client.get(f"{prefix}/information")
    json_data = json.loads(response.content)
    assert response.status_code == 200
    assert json_data == {"CRITICAL": "Development in progress. Sorry, this challenge is not ready yet."}


