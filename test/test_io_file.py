from __future__ import annotations

import hashlib

import pytest

from hmpy.io import LocalFile


def test_create_makes_empty_file_and_parent_directories(tmp_path) -> None:
    path = tmp_path / "nested" / "source.txt"

    created = LocalFile.create(str(path), create_parent_dir=True)

    assert created.exists
    assert created.size_in_bytes == 0
    assert path.exists()


def test_create_rejects_existing_file(tmp_path) -> None:
    path = tmp_path / "source.txt"
    path.write_text("content", encoding="utf8")

    with pytest.raises(IOError, match="already exists"):
        LocalFile.create(str(path))


def test_delete_removes_existing_file(tmp_path) -> None:
    path = tmp_path / "source.txt"
    path.write_text("content", encoding="utf8")

    LocalFile.delete(str(path))

    assert not path.exists()


def test_delete_rejects_missing_file(tmp_path) -> None:
    with pytest.raises(IOError, match="not found"):
        LocalFile.delete(str(tmp_path / "missing.txt"))


def test_copy_duplicates_file_contents(tmp_path) -> None:
    source_path = tmp_path / "source.txt"
    copied_path = tmp_path / "copy.txt"
    source_path.write_text("hello hmpy\n", encoding="utf8")

    copied = LocalFile.copy(str(source_path), str(copied_path))

    assert copied.exists
    assert copied_path.read_text(encoding="utf8") == "hello hmpy\n"


def test_copy_rejects_missing_source(tmp_path) -> None:
    with pytest.raises(IOError, match="not found"):
        LocalFile.copy(str(tmp_path / "missing.txt"), str(tmp_path / "copy.txt"))


def test_copy_rejects_existing_destination(tmp_path) -> None:
    source_path = tmp_path / "source.txt"
    dest_path = tmp_path / "copy.txt"
    source_path.write_text("content", encoding="utf8")
    dest_path.write_text("existing", encoding="utf8")

    with pytest.raises(IOError, match="already exists"):
        LocalFile.copy(str(source_path), str(dest_path))


def test_move_relocates_file_and_creates_destination_directory(tmp_path) -> None:
    source_path = tmp_path / "source.txt"
    moved_path = tmp_path / "nested" / "moved.txt"
    source_path.write_text("content", encoding="utf8")

    moved = LocalFile.move(str(source_path), str(moved_path), create_dir=True)

    assert moved.exists
    assert not source_path.exists()
    assert moved_path.read_text(encoding="utf8") == "content"


def test_move_rejects_missing_source(tmp_path) -> None:
    with pytest.raises(IOError, match="not found"):
        LocalFile.move(str(tmp_path / "missing.txt"), str(tmp_path / "dest.txt"))


def test_move_rejects_existing_destination(tmp_path) -> None:
    source_path = tmp_path / "source.txt"
    dest_path = tmp_path / "dest.txt"
    source_path.write_text("content", encoding="utf8")
    dest_path.write_text("existing", encoding="utf8")

    with pytest.raises(IOError, match="already exists"):
        LocalFile.move(str(source_path), str(dest_path))


def test_file_metadata_and_hashes_are_reported_exactly(tmp_path) -> None:
    path = tmp_path / "source.txt"
    path.write_text("hello hmpy\n", encoding="utf8")

    file = LocalFile(str(path))

    assert file.filename_without_extension == "source"
    assert file.extension == ".txt"
    assert file.size_in_bytes == len("hello hmpy\n".encode("utf8"))
    assert file.get_md5() == hashlib.md5(b"hello hmpy\n").hexdigest()
    assert file.get_sha256() == hashlib.sha256(b"hello hmpy\n").hexdigest()


def test_file_metadata_for_extensionless_file(tmp_path) -> None:
    path = tmp_path / "source"
    path.write_text("content", encoding="utf8")

    file = LocalFile(str(path))

    assert file.filename_without_extension == "source"
    assert file.extension == ""