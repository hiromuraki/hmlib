from typing import Any, Generic, TypeVar, Iterable, Iterator, Callable, overload


T = TypeVar("T")
TOut = TypeVar("TOut")


class ArrayList(Generic[T]):
    def __init__(self, items: Iterable[T] | None = None) -> None:
        if items is None:
            items = []
        self.__list: list[T] = [x for x in items]

    @property
    def count(self) -> int:
        return len(self.__list)

    def contains(self, item: T) -> bool:
        return item in self.__list

    def add(self, item: T) -> "ArrayList[T]":
        self.__list.append(item)
        return self

    def remove(self, item: T) -> "ArrayList[T]":
        self.__list.remove(item)
        return self

    def take(self, count: int) -> "ArrayList[T]":
        return ArrayList(self.__list[:count])

    def clear(self) -> None:
        self.__list.clear()

    def index_of(self, item: T) -> int:
        return self.__list.index(item)

    def map(self, func: Callable[[T], TOut]) -> "ArrayList[TOut]":
        return ArrayList(func(x) for x in self.__list)

    def reduce(self, func: Callable[[T, T], T]) -> T | None:
        if len(self.__list) == 0:
            return None

        accumulate = self.__list[0]
        for item in self.__list[1:]:
            accumulate = func(accumulate, item)

        return accumulate

    def filter(self, predicate: Callable[[T], bool]) -> "ArrayList[T]":
        return ArrayList(x for x in self.__list if predicate(x))

    def order(self, key_selector: Callable[[T], Any]) -> "ArrayList[T]":
        return ArrayList(sorted(self.__list, key=key_selector))

    def to_py_list(self) -> list[T]:
        return [x for x in self.__list]

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> "ArrayList[T]": ...

    def __getitem__(self, index: int | slice) -> T | "ArrayList[T]":
        if isinstance(index, slice):
            return ArrayList(self.__list[index])
        else:
            return self.__list[index]

    def __setitem__(self, index: int, value: T) -> None:
        self.__list[index] = value

    def __iter__(self) -> Iterator[T]:
        return self.__list.__iter__()

    def __str__(self) -> str:
        return self.__list.__str__()

    def __reduce__(self) -> str | tuple[Any, ...]:
        return self.__str__()

    def __len__(self):
        return len(self.__list)
