import requests

from tests_api.constants import BASE_URL, REACTOR_PATH, RESET_PROGRESS_MESSAGE, DIDNT_SEE_THE_GRAPHITE_FLAG
from tests_api.models.commander import Commander

commander = Commander()


def test_reset_progress():
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/reset_progress")
    assert response.status_code == 200
    assert response.json()["message"] == RESET_PROGRESS_MESSAGE
    assert response.json()["flag"] == DIDNT_SEE_THE_GRAPHITE_FLAG
