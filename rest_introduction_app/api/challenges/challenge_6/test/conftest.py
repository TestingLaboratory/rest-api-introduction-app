import pytest

from rest_introduction_app.api.challenges.challenge_6.model import Storage


@pytest.fixture()
def empty_backpack():
    return Storage("backpack", 3)


@pytest.fixture()
def two_items_backpack():
    return Storage("backpack", 3, ["tent", "knife"])


STORAGE_TYPE = "backpack"
MAX_ITEMS = 3

not_full_backpacks = [
    Storage(STORAGE_TYPE, MAX_ITEMS, []),
    Storage(STORAGE_TYPE, MAX_ITEMS, ["tent", "knife"]),
]

full_backpacks = [
    Storage(STORAGE_TYPE, MAX_ITEMS, ["tent", "knife", "lighter"]),
    Storage(STORAGE_TYPE, MAX_ITEMS, ["tent", "knife", "lighter", "camera"])
]
