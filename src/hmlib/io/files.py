from pathlib import Path
from typing import Iterable
from ..collection import ArrayList


class TextFile:
    def __init__(self, path: str | Path, encoding: str = "utf8", newline: str = "\n"):
        if isinstance(path, str):
            path = Path(path)

        self.__path: Path = path.resolve()
        self.__encoding: str = encoding
        self.__newline: str = newline

        if self.__path.exists():
            with open(self.__path, mode="r", encoding=encoding, newline=newline) as fp:
                self.__lines = fp.read().splitlines()
        else:
            self.__lines = []

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def content(self) -> str:
        return "\n".join(self.__lines)

    def enumerate_lines(self) -> Iterable[str]:
        for line in self.__lines:
            yield line

    def get_lines(self) -> ArrayList[str]:
        return ArrayList(self.enumerate_lines())

    def get_line(self, index: int) -> str:
        return self.__lines[index]

    def append_line(self, line: str) -> "TextFile":
        self.__lines.append(line)

        return self

    def append_lines(self, lines: Iterable[str]) -> "TextFile":
        for line in lines:
            self.__lines.append(line)

        return self

    def clear(self) -> "TextFile":
        self.__lines.clear()
        return self

    def commit_changes(self) -> "TextFile":
        with open(
            self.path, mode="w", encoding=self.__encoding, newline=self.__newline
        ) as fp:
            for line in self.__lines:
                fp.write(line + self.__newline)
        return self
