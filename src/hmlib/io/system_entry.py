from ..collection.list import List
from typing import Iterable
from pathlib import Path
from typing import Any, Optional
from ..datetime import DateTime
from io import FileIO
import hashlib
import os
import shutil


class SystemEntry:
    def __init__(self, path: str | Path):
        if isinstance(path, str):
            path = Path(path)

        self.__path: Path = path.resolve()

    @property
    def absolute_path(self) -> Path:
        return self.__path

    @property
    def parent_directory(self) -> "LocalDirectory":
        return LocalDirectory(self.__path.parent)

    @property
    def filename(self) -> str:
        return self.__path.name


class LocalFile(SystemEntry):
    def __init__(self, path: str | Path):
        super().__init__(path)

        self.__sha256: Optional[str] = None
        self.__md5: Optional[str] = None

    @classmethod
    def create(cls, filepath: str, create_parent_dir: bool = False) -> "LocalFile":
        if LocalFile(filepath).exists:
            raise IOError(f"{filepath} already exists")

        if create_parent_dir:
            cls.__ensure_directory_exits(filepath)

        open(filepath, mode="wb").close()
        return LocalFile(filepath)

    @classmethod
    def delete(cls, filepath: str):
        if not LocalFile(filepath).exists:
            raise IOError(f"{filepath} not found")

        os.remove(filepath)

    @classmethod
    def copy(cls, src_filepath: str, dest_filepath) -> "LocalFile":
        if not LocalFile(src_filepath).exists:
            raise IOError(f"{src_filepath} not found")
        if LocalFile(dest_filepath).exists:
            raise IOError(f"{dest_filepath} already exists")

        shutil.copyfile(src_filepath, dest_filepath)
        return LocalFile(dest_filepath)

    @classmethod
    def move(
        cls, src_filepath: str, dest_filepath, create_dir: bool = False
    ) -> "LocalFile":
        if not LocalFile(src_filepath).exists:
            raise IOError(f"{src_filepath} not found")
        if LocalFile(dest_filepath).exists:
            raise IOError(f"{dest_filepath} already exists")

        if create_dir:
            cls.__ensure_directory_exits(dest_filepath)

        shutil.move(src_filepath, dest_filepath)
        return LocalFile(dest_filepath)

    @property
    def exists(self) -> bool:
        return self.absolute_path.exists() and self.absolute_path.is_file()

    @property
    def filename_without_extension(self) -> str:
        return self.absolute_path.stem

    @property
    def extension(self) -> str:
        """
        获取文件的扩展名（包括点号，例如 `.txt`）。

        :return: 文件的扩展名
        """
        return self.absolute_path.suffix

    @property
    def size_in_bytes(self) -> int:
        """
        获取文件大小，以字节为单位。

        :return: 文件大小（单位字节）
        """
        if self.exists:
            return os.path.getsize(self.absolute_path)

        return -1

    @property
    def create_date_time(self) -> DateTime:
        return DateTime(os.path.getctime(self.absolute_path))

    @property
    def update_date_time(self) -> DateTime:
        return DateTime(os.path.getmtime(self.absolute_path))

    @property
    def access_date_time(self) -> DateTime:
        return DateTime(os.path.getatime(self.absolute_path))

    def get_md5(self) -> str:
        if self.__md5 is None:
            self.__md5 = self.__calculate_hash(Path(self.absolute_path), hashlib.md5())

        return self.__md5

    def get_sha256(self) -> str:
        if self.__sha256 is None:
            self.__sha256 = self.__calculate_hash(
                Path(self.absolute_path), hashlib.sha256()
            )

        return self.__sha256

    def __str__(self):
        return f"LocalFile({self.absolute_path})"

    @classmethod
    def __ensure_directory_exits(cls, filepath: str) -> None:
        dir_name = os.path.dirname(filepath)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    @classmethod
    def __calculate_hash(cls, filepath: Path, hash: Any) -> str:
        buffer = bytearray(65536)
        fio = FileIO(filepath)
        while True:
            read_count = fio.readinto(buffer)
            if read_count == 0:
                break

            if read_count == 65536:
                hash.update(buffer)
            else:
                hash.update(buffer[0:read_count])

        return hash.hexdigest()


class LocalDirectory(SystemEntry):
    def __init__(self, path: str | Path):
        super().__init__(path)

    @classmethod
    def create(cls, path: str) -> None:
        os.makedirs(path, exist_ok=True)

    def exists(self) -> bool:
        return self.absolute_path.exists() and self.absolute_path.is_dir()

    def enumerate_files(self, recursive: bool = False) -> Iterable[LocalFile]:
        for root, _, files in os.walk(self.absolute_path):
            for file in files:
                yield LocalFile(os.path.join(root, file))
            if not recursive:
                break  # 仅遍历顶层目录

    def get_files(self, recursive: bool = False) -> List[LocalFile]:
        return List(self.enumerate_files(recursive))

    def enumerate_directories(
        self, recursive: bool = False
    ) -> Iterable["LocalDirectory"]:
        for root, dirs, _ in os.walk(self.absolute_path):
            for dir in dirs:
                yield LocalDirectory(os.path.join(root, dir))
            if not recursive:
                break  # 仅遍历顶层目录

    def get_directories(self, recursive: bool = False) -> List["LocalDirectory"]:
        return List(self.enumerate_directories(recursive))
