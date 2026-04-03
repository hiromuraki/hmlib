from __future__ import annotations

import datetime as py_datetime
import importlib

import pytest

from hmlib.DateTime import DateTime


datetime_module = importlib.import_module("hmlib.DateTime")


def test_from_datetime_uses_defaults_when_arguments_are_omitted() -> None:
    value = DateTime.from_datetime()

    assert value.unix_timestamp == py_datetime.datetime(1970, 1, 1).timestamp()
    assert str(value) == "1970-01-01 00:00:00"


def test_from_datetime_preserves_exact_calendar_values() -> None:
    value = DateTime.from_datetime(2024, 2, 29, 23, 59, 59, 999)

    expected = py_datetime.datetime(2024, 2, 29, 23, 59, 59, 999000).timestamp()

    assert value.unix_timestamp == expected
    assert value.year == 2024
    assert value.month == 2
    assert value.day == 29
    assert value.hour == 23
    assert value.minute == 59
    assert value.second == 59
    assert hash(value) == int(expected)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"month": 0}, "month must be between 1 and 12"),
        ({"month": 13}, "month must be between 1 and 12"),
        ({"day": 0}, "day must be between 1 and 31"),
        ({"day": 32}, "day must be between 1 and 31"),
        ({"hour": -1}, "hour must be between 0 and 23"),
        ({"hour": 24}, "hour must be between 0 and 23"),
        ({"minute": -1}, "minute must be between 0 and 59"),
        ({"minute": 60}, "minute must be between 0 and 59"),
        ({"second": -1}, "second must be between 0 and 59"),
        ({"second": 60}, "second must be between 0 and 59"),
        ({"millisecond": -1}, "millisecond must be between 0 and 999"),
        ({"millisecond": 1000}, "millisecond must be between 0 and 999"),
    ],
)
def test_from_datetime_rejects_out_of_range_components(kwargs: dict[str, int], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        DateTime.from_datetime(**kwargs)


def test_from_datetime_rejects_invalid_calendar_dates() -> None:
    with pytest.raises(ValueError, match="Invalid datetime parameters"):
        DateTime.from_datetime(2023, 2, 29)


def test_now_reads_current_epoch_seconds(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(datetime_module.time, "time", lambda: 123.5)

    assert DateTime.now().unix_timestamp == 123.5


def test_comparison_operators_compare_timestamp_values() -> None:
    left = DateTime.from_datetime(2024, 1, 1, 0, 0, 0, 0)
    right = DateTime.from_datetime(2024, 1, 1, 0, 0, 1, 0)

    assert left < right
    assert right > left
    assert left == DateTime(left.unix_timestamp)


def test_constructor_rejects_non_float_timestamp() -> None:
    with pytest.raises(ValueError, match="timestamp must be a float"):
        DateTime(1)