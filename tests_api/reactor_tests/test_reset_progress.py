import requests

from tests_api.constants import BASE_URL, REACTOR_PATH, RESET_PROGRESS_MESSAGE, DIDNT_SEE_THE_GRAPHITE_FLAG


def test_reset_progress(commander):
    commander.obtain_a_key()
    response = requests.get(f"{BASE_URL}/{REACTOR_PATH}/{commander.key}/reset_progress")
    assert response.status_code == 200
    assert response.json()["message"] == RESET_PROGRESS_MESSAGE
    assert response.json()["flag"] == DIDNT_SEE_THE_GRAPHITE_FLAG
