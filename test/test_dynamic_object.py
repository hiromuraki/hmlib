from __future__ import annotations

import pytest

from hmpy.DynamicObject import DynamicObject


def test_getattr_reads_nested_dict_values() -> None:
    value = DynamicObject({"name": "Ada", "meta": {"age": 30}})

    assert value.name.str() == "Ada"
    assert value.meta.age.int() == 30


def test_getattr_returns_none_wrapper_for_missing_dict_key() -> None:
    value = DynamicObject({"name": "Ada"})

    assert value.missing.is_none()


def test_getattr_returns_none_wrapper_for_non_mapping_object() -> None:
    value = DynamicObject("text")

    assert value.anything.is_none()


def test_getattr_returns_none_wrapper_for_none_object() -> None:
    value = DynamicObject(None)

    assert value.anything.is_none()


def test_int_accessor_accepts_only_exact_int() -> None:
    assert DynamicObject(1).int() == 1


@pytest.mark.parametrize("wrapped", [True, 1.5, "1", None])
def test_int_accessor_rejects_non_int_values(wrapped: object) -> None:
    with pytest.raises(ValueError):
        DynamicObject(wrapped).int()


def test_float_accessor_accepts_only_exact_float() -> None:
    assert DynamicObject(1.5).float() == 1.5


@pytest.mark.parametrize("wrapped", [1, True, "1.5", None])
def test_float_accessor_rejects_non_float_values(wrapped: object) -> None:
    with pytest.raises(ValueError):
        DynamicObject(wrapped).float()


def test_str_accessor_accepts_only_exact_string() -> None:
    assert DynamicObject("hello").str() == "hello"


@pytest.mark.parametrize("wrapped", [1, True, 1.5, None])
def test_str_accessor_rejects_non_string_values(wrapped: object) -> None:
    with pytest.raises(ValueError):
        DynamicObject(wrapped).str()


def test_bool_accessor_accepts_only_exact_bool() -> None:
    assert DynamicObject(True).bool() is True


@pytest.mark.parametrize("wrapped", [1, 0, 1.0, "true", None])
def test_bool_accessor_rejects_non_bool_values(wrapped: object) -> None:
    with pytest.raises(ValueError):
        DynamicObject(wrapped).bool()