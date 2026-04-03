from __future__ import annotations

import pytest

from hmpy.collection import List


def test_count_reflects_initial_items() -> None:
    assert List([3, 1, 2]).count == 3


def test_contains_matches_existing_item() -> None:
    assert List([3, 1, 2]).contains(1)


def test_add_returns_same_instance_and_appends_item() -> None:
    values = List([3, 1, 2])

    assert values.add(4) is values
    assert values.to_py_list() == [3, 1, 2, 4]


def test_remove_deletes_exact_item() -> None:
    values = List([1, 2, 3])

    assert values.remove(2).to_py_list() == [1, 3]


def test_remove_raises_for_missing_item() -> None:
    with pytest.raises(ValueError):
        List([1, 2, 3]).remove(4)


def test_take_returns_new_list_without_mutating_source() -> None:
    values = List([1, 2, 3, 4])

    taken = values.take(2)

    assert taken.to_py_list() == [1, 2]
    assert values.to_py_list() == [1, 2, 3, 4]


def test_take_with_negative_count_uses_python_slice_semantics() -> None:
    assert List([1, 2, 3, 4]).take(-1).to_py_list() == [1, 2, 3]


def test_clear_empties_the_list() -> None:
    values = List([1, 2, 3])

    values.clear()

    assert values.count == 0
    assert values.to_py_list() == []


def test_index_of_returns_exact_position() -> None:
    assert List([3, 1, 2]).index_of(2) == 2


def test_index_of_raises_for_missing_item() -> None:
    with pytest.raises(ValueError):
        List([1, 2, 3]).index_of(4)


def test_map_returns_transformed_list() -> None:
    assert List([3, 1, 2]).map(lambda item: item * 2).to_py_list() == [6, 2, 4]


def test_reduce_returns_none_for_empty_list() -> None:
    assert List[int]().reduce(lambda left, right: left + right) is None


def test_reduce_folds_values_left_to_right() -> None:
    assert List([3, 1, 2]).reduce(lambda left, right: left - right) == 0


def test_filter_keeps_only_matching_items() -> None:
    assert List([3, 1, 2, 4]).filter(lambda item: item % 2 == 0).to_py_list() == [2, 4]


def test_order_sorts_using_key_selector() -> None:
    assert List([3, 1, 2, 4]).order(lambda item: item).to_py_list() == [1, 2, 3, 4]


def test_slice_returns_new_list() -> None:
    assert List([3, 1, 2, 4])[1:3].to_py_list() == [1, 2]


def test_item_assignment_overwrites_existing_slot() -> None:
    values = List([3, 1, 2])

    values[1] = 10

    assert values.to_py_list() == [3, 10, 2]