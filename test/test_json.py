from __future__ import annotations

import json

import pytest

from hmpy.text.Json import Json


def test_parse_file_reads_json_object(tmp_path) -> None:
    json_path = tmp_path / "data.json"
    json_path.write_text('{"name": "Ada", "count": 3}', encoding="utf8")

    parsed = Json.parse_file(str(json_path))

    assert parsed.name.str() == "Ada"
    assert parsed.count.int() == 3


def test_parse_file_raises_for_invalid_json(tmp_path) -> None:
    json_path = tmp_path / "invalid.json"
    json_path.write_text("{", encoding="utf8")

    with pytest.raises(json.JSONDecodeError):
        Json.parse_file(str(json_path))


def test_to_json_serializes_plain_object() -> None:
    assert Json.to_json({"name": "Ada"}) == '{"name": "Ada"}'


def test_to_json_raises_for_non_serializable_object() -> None:
    with pytest.raises(TypeError):
        Json.to_json(object())