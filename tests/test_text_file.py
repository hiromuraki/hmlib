from __future__ import annotations

from hmpy.io import TextFile


def test_text_file_reads_existing_file_as_plain_lines(tmp_path) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("alpha\nbeta\n", encoding="utf8")

    text_file = TextFile(str(path))

    assert text_file.path == path.resolve()
    assert text_file.get_lines().to_py_list() == ["alpha", "beta"]
    assert text_file.get_line(0) == "alpha"
    assert text_file.get_line(1) == "beta"
    assert text_file.content == "alpha\nbeta"


def test_text_file_handles_empty_existing_file(tmp_path) -> None:
    path = tmp_path / "empty.txt"
    path.write_text("", encoding="utf8")

    text_file = TextFile(str(path))

    assert text_file.get_lines().to_py_list() == []
    assert text_file.content == ""


def test_text_file_starts_empty_for_missing_file(tmp_path) -> None:
    text_file = TextFile(str(tmp_path / "missing.txt"))

    assert text_file.get_lines().to_py_list() == []
    assert text_file.content == ""


def test_text_file_append_line_updates_in_memory_state(tmp_path) -> None:
    text_file = TextFile(str(tmp_path / "append.txt"))

    assert text_file.append_line("alpha") is text_file
    assert text_file.get_lines().to_py_list() == ["alpha"]
    assert text_file.content == "alpha"


def test_text_file_append_lines_keeps_order(tmp_path) -> None:
    text_file = TextFile(str(tmp_path / "append.txt"))

    assert text_file.append_lines(["alpha", "beta"]) is text_file
    assert text_file.get_lines().to_py_list() == ["alpha", "beta"]


def test_text_file_clear_removes_all_lines(tmp_path) -> None:
    text_file = TextFile(str(tmp_path / "clear.txt"))
    text_file.append_lines(["alpha", "beta"])

    assert text_file.clear() is text_file
    assert text_file.get_lines().to_py_list() == []
    assert text_file.content == ""


def test_text_file_commit_changes_writes_normalized_newlines(tmp_path) -> None:
    path = tmp_path / "commit.txt"
    text_file = TextFile(str(path))
    text_file.append_lines(["alpha", "beta"])

    assert text_file.commit_changes() is text_file
    assert path.read_text(encoding="utf8") == "alpha\nbeta\n"


def test_text_file_round_trips_after_commit(tmp_path) -> None:
    path = tmp_path / "roundtrip.txt"

    text_file = TextFile(str(path))
    text_file.append_lines(["alpha", "beta"]).commit_changes()

    reloaded = TextFile(str(path))

    assert reloaded.get_lines().to_py_list() == ["alpha", "beta"]
    assert reloaded.content == "alpha\nbeta"