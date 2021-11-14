import pytest


from rest_introduction_app.api.challenges.challenge_6.model import Storage, ItemName, Item, Hiker, is_pocket_size, \
    add_item, remove_item, put_items, swap_item, is_full
from rest_introduction_app.api.challenges.challenge_6.test.utils import not_full_backpacks, full_backpacks


def test_item_model_is_pocket_size_true():
    pocket_size_item = Item(name=ItemName.map)
    assert is_pocket_size(pocket_size_item)


def test_add_item_increases_content_by_one(empty_backpack):
    initial_number_of_items = len(empty_backpack.content)
    tent = ItemName("tent")
    add_item(empty_backpack, tent)
    actual_number_of_items = len(empty_backpack.content)
    assert actual_number_of_items == initial_number_of_items + 1


def test_remove_item_decreases_content_by_one(two_items_backpack):
    initial_number_of_items = len(two_items_backpack.content)
    item_to_remove = two_items_backpack.content[0]
    remove_item(two_items_backpack, item_to_remove)
    actual_number_of_items = len(two_items_backpack.content)
    assert actual_number_of_items == initial_number_of_items - 1


def test_put_items_replaces_list_of_contents(two_items_backpack, three_items):
    initial_items_in_backpack = two_items_backpack.content
    put_items(two_items_backpack, three_items)
    assert initial_items_in_backpack not in two_items_backpack.content
    assert two_items_backpack.content == three_items


def test_swap_item_replaces_one_item(two_items_backpack):
    item_to_replace = ItemName("tent")
    item_to_pack = ItemName("camera")
    swap_item(two_items_backpack, item_to_replace, item_to_pack)
    assert item_to_pack in two_items_backpack.content
    assert item_to_replace not in two_items_backpack.content


@pytest.mark.parametrize("backpack", not_full_backpacks)
def test_backpack_is_full_returns_false(backpack):
    assert not is_full(backpack)


@pytest.mark.parametrize("backpack", full_backpacks)
def test_backpack_is_full_returns_true(backpack):
    assert is_full(backpack)
