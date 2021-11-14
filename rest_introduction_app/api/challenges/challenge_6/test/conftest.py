import pytest

from rest_introduction_app.api.challenges.challenge_6.model import Storage, ItemName, Item


@pytest.fixture()
def item_model():
    return Item()


@pytest.fixture()
def empty_backpack():
    return Storage("backpack", 3)


@pytest.fixture()
def two_items_backpack():
    return Storage("backpack", 3, ["tent", "knife"])


@pytest.fixture()
def three_items() -> list[ItemName]:
    return [ItemName["lighter"], ItemName["camera"], ItemName["knife"]]
