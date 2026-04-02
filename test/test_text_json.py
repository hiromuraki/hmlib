from __future__ import annotations

import json

import pytest

from hmpy.text import Json


def test_parse_reads_json_object_from_string() -> None:
    parsed = Json.parse('{"name": "Ada", "meta": {"count": 3}}')

    assert parsed.name.str() == "Ada"
    assert parsed.meta.count.int() == 3


def test_parse_reads_empty_object() -> None:
    parsed = Json.parse("{}")

    assert parsed.is_none() is False
    assert parsed.missing.is_none()


def test_parse_raises_for_invalid_json_text() -> None:
    with pytest.raises(json.JSONDecodeError):
        Json.parse("{")


def test_to_json_serializes_plain_object() -> None:
    assert Json.to_json({"name": "Ada", "tags": ["a", "b"]}) == '{"name": "Ada", "tags": ["a", "b"]}'


def test_to_json_raises_for_non_serializable_object() -> None:
    with pytest.raises(TypeError):
        Json.to_json(object())