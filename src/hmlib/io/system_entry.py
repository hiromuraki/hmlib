from ..collection.list import ArrayList
from typing import Iterable
from pathlib import Path
from typing import Any, Optional
from ..datetime import DateTime
from io import FileIO
import hashlib
import os
import shutil
import stat


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
    def create(cls, filepath: Path | str, create_parent_dir: bool = False) -> "LocalFile":
        if LocalFile(filepath).exists:
            raise IOError(f"{filepath} already exists")

        if create_parent_dir:
            cls.__ensure_directory_exits(filepath)

        open(filepath, mode="wb").close()
        return LocalFile(filepath)

    @classmethod
    def delete(cls, filepath: Path | str):
        if not LocalFile(filepath).exists:
            raise IOError(f"{filepath} not found")

        os.remove(filepath)

    @classmethod
    def copy(cls, src_filepath: Path | str, dest_filepath: Path | str) -> "LocalFile":
        if not LocalFile(src_filepath).exists:
            raise IOError(f"{src_filepath} not found")
        if LocalFile(dest_filepath).exists:
            raise IOError(f"{dest_filepath} already exists")

        shutil.copyfile(src_filepath, dest_filepath)
        return LocalFile(dest_filepath)

    @classmethod
    def move(
        cls,
        src_filepath: Path | str,
        dest_filepath: Path | str,
        create_dir: bool = False,
    ) -> "LocalFile":
        if not LocalFile(src_filepath).exists:
            raise IOError(f"{src_filepath} not found")
        if LocalFile(dest_filepath).exists:
            raise IOError(f"{dest_filepath} already exists")

        if create_dir:
            cls.__ensure_directory_exits(dest_filepath)

        shutil.move(src_filepath, dest_filepath)
        return LocalFile(dest_filepath)

    @classmethod
    def compare_equality(cls, file1: "LocalFile | Path | str", file2: "LocalFile | Path | str") -> bool:
        if not isinstance(file1, LocalFile):
            file1 = LocalFile(file1)
        if not isinstance(file2, LocalFile):
            file2 = LocalFile(file2)

        try:
            stat1 = os.stat(file1.absolute_path)
            stat2 = os.stat(file2.absolute_path)
        except OSError as e:
            raise IOError(f"Error accessing file: {e}")

        # 2. 安全性检查：确保两个都是常规文件 (避免管道、设备文件导致无限阻塞)
        if not (stat.S_ISREG(stat1.st_mode) and stat.S_ISREG(stat2.st_mode)):
            raise ValueError("Both paths must be regular files.")

        # 3. 操作系统层面的同源判断 (处理硬链接和符号链接，极大地提升可靠性和性能)
        if os.path.samestat(stat1, stat2):
            return True

        # 判断规则
        # 1. 如果两个文件的绝对路径相同，则认为它们是相同的文件
        # 2. 如果两个文件的大小不同，则认为它们是不同的文件
        # 3. 其余情况，则逐字节对比
        if file1.absolute_path == file2.absolute_path:
            return True

        if file1.size_in_bytes != file2.size_in_bytes:
            return False

        try:
            buffer_size = 16 * 1024
            with (
                open(file1.absolute_path, "rb") as f1,
                open(file2.absolute_path, "rb") as f2,
            ):
                while True:
                    chunk1 = f1.read(buffer_size)
                    chunk2 = f2.read(buffer_size)

                    if chunk1 != chunk2:
                        return False

                    if not chunk1:
                        break
        except OSError as e:
            raise IOError(f"Error reading files during comparison: {e}")
        return True

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
    def create_datetime(self) -> DateTime:
        return DateTime(os.path.getctime(self.absolute_path))

    @property
    def update_datetime(self) -> DateTime:
        return DateTime(os.path.getmtime(self.absolute_path))

    @property
    def access_datetime(self) -> DateTime:
        return DateTime(os.path.getatime(self.absolute_path))

    def get_md5(self) -> str:
        if self.__md5 is None:
            self.__md5 = self.__calculate_hash(Path(self.absolute_path), hashlib.md5())

        return self.__md5

    def get_sha256(self) -> str:
        if self.__sha256 is None:
            self.__sha256 = self.__calculate_hash(Path(self.absolute_path), hashlib.sha256())

        return self.__sha256

    def __str__(self):
        return f"LocalFile({self.absolute_path})"

    @classmethod
    def __ensure_directory_exits(cls, filepath: Path | str) -> None:
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
    def __init__(self, path: Path | str):
        super().__init__(path)

    @classmethod
    def create(cls, path: Path | str) -> None:
        os.makedirs(path, exist_ok=True)

    def exists(self) -> bool:
        return self.absolute_path.exists() and self.absolute_path.is_dir()

    def enumerate_files(self, recursive: bool = False) -> Iterable[LocalFile]:
        for root, _, files in os.walk(self.absolute_path):
            for file in files:
                yield LocalFile(os.path.join(root, file))
            if not recursive:
                break  # 仅遍历顶层目录

    def get_files(self, recursive: bool = False) -> ArrayList[LocalFile]:
        return ArrayList(self.enumerate_files(recursive))

    def enumerate_directories(self, recursive: bool = False) -> Iterable["LocalDirectory"]:
        for root, dirs, _ in os.walk(self.absolute_path):
            for dir in dirs:
                yield LocalDirectory(os.path.join(root, dir))
            if not recursive:
                break  # 仅遍历顶层目录

    def get_directories(self, recursive: bool = False) -> ArrayList["LocalDirectory"]:
        return ArrayList(self.enumerate_directories(recursive))
