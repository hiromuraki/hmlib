from __future__ import annotations

import re

import pytest

from hmpy.text.Regex import Regex


def test_is_match_returns_true_for_full_match() -> None:
    assert Regex.is_match(r"\d+", "123")


def test_is_match_returns_false_for_partial_match() -> None:
    assert not Regex.is_match(r"\d+", "123a")


def test_is_match_returns_false_for_invalid_pattern() -> None:
    assert not Regex.is_match(r"[", "text")


def test_match_returns_match_object_for_prefix_match() -> None:
    result = Regex.match(r"\d+", "123abc")
    assert result is not None
    assert result.group(0) == "123"


def test_match_returns_none_when_text_does_not_match() -> None:
    assert Regex.match(r"\d+", "abc") is None


def test_match_raises_for_invalid_pattern() -> None:
    with pytest.raises(re.error):
        Regex.match(r"[", "text")
