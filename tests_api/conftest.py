import pytest

from tests_api.models.commander import Commander


@pytest.fixture()
def commander():
    return Commander()
