from __future__ import annotations

from hmlib.io import LocalDirectory


def test_directory_exists_only_for_directories(tmp_path) -> None:
    directory = LocalDirectory(str(tmp_path))
    file_path = tmp_path / "file.txt"
    file_path.write_text("content", encoding="utf8")

    assert directory.exists()
    assert not LocalDirectory(str(file_path)).exists()


def test_directory_absolute_path_is_normalized(tmp_path) -> None:
    directory = LocalDirectory(str(tmp_path / "nested" / ".."))

    assert directory.absolute_path == (tmp_path / "nested" / "..").resolve()


def test_directory_parent_directory_points_to_parent(tmp_path) -> None:
    directory = LocalDirectory(str(tmp_path))

    assert directory.parent_directory.absolute_path == tmp_path.parent.resolve()


def test_get_files_returns_only_top_level_entries_by_default(tmp_path) -> None:
    (tmp_path / "root.txt").write_text("root", encoding="utf8")
    child_dir = tmp_path / "child"
    child_dir.mkdir()
    (child_dir / "nested.txt").write_text("nested", encoding="utf8")

    files = LocalDirectory(str(tmp_path)).get_files().to_py_list()

    assert {file.filename for file in files} == {"root.txt"}


def test_get_files_recurses_when_requested(tmp_path) -> None:
    (tmp_path / "root.txt").write_text("root", encoding="utf8")
    child_dir = tmp_path / "child"
    child_dir.mkdir()
    (child_dir / "nested.txt").write_text("nested", encoding="utf8")

    files = LocalDirectory(str(tmp_path)).get_files(recursive=True).to_py_list()

    assert {file.filename for file in files} == {"root.txt", "nested.txt"}


def test_get_directories_returns_only_top_level_entries_by_default(tmp_path) -> None:
    (tmp_path / "child").mkdir()
    (tmp_path / "child" / "grandchild").mkdir()

    directories = LocalDirectory(str(tmp_path)).get_directories().to_py_list()

    assert {directory.filename for directory in directories} == {"child"}


def test_get_directories_recurses_when_requested(tmp_path) -> None:
    (tmp_path / "child").mkdir()
    (tmp_path / "child" / "grandchild").mkdir()

    directories = LocalDirectory(str(tmp_path)).get_directories(recursive=True).to_py_list()

    assert {directory.filename for directory in directories} == {"child", "grandchild"}