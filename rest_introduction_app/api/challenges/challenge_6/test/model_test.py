import pytest
from rest_introduction_app.api.challenges.challenge_6.model import Storage, Item
from rest_introduction_app.api.challenges.challenge_6.test.conftest import not_full_backpacks, full_backpacks


def test_add_item_increases_content_by_one(empty_backpack):
    initial_number_of_items = len(empty_backpack.content)
    tent = Item("tent")
    empty_backpack.add_item(tent)
    actual_number_of_items = len(empty_backpack.content)
    assert actual_number_of_items == initial_number_of_items + 1
    assert tent in empty_backpack.content


def test_remove_item_decreases_content_by_one(two_items_backpack):
    initial_number_of_items = len(two_items_backpack.content)
    item_to_remove = two_items_backpack.content[0]
    two_items_backpack.remove_item(item_to_remove)
    actual_number_of_items = len(two_items_backpack.content)
    assert actual_number_of_items == initial_number_of_items - 1


def test_put_items_replaces_list_of_contents(two_items_backpack):
    initial_item_in_backpack = two_items_backpack.content
    list_of_items_to_put = ["lighter", "camera", "knife"]
    two_items_backpack.put_items(list_of_items_to_put)
    assert initial_item_in_backpack not in two_items_backpack.content
    assert two_items_backpack.content == list_of_items_to_put


def test_swap_item_replaces_one_item(two_items_backpack):
    item_to_replace = Item("tent")
    item_to_pack = Item("camera")
    two_items_backpack.swap_item(item_to_replace, item_to_pack)
    assert item_to_pack in two_items_backpack.content
    assert item_to_replace not in two_items_backpack.content


@pytest.mark.parametrize("backpack", not_full_backpacks)
def test_backpack_is_full_returns_false(backpack):
    assert not backpack.is_full()


@pytest.mark.parametrize("backpack", full_backpacks)
def test_backpack_is_full_returns_true(backpack):
    assert backpack.is_full()

