from typing import Any, Generic, TypeVar, Iterable, Iterator, Callable, overload


T = TypeVar("T")
TOut = TypeVar("TOut")


class List(Generic[T]):
    def __init__(self, items: Iterable[T] | None = None) -> None:
        if items is None:
            items = []
        self.__list: list[T] = [x for x in items]

    @property
    def count(self) -> int:
        return len(self.__list)

    def contains(self, item: T) -> bool:
        return item in self.__list

    def add(self, item: T) -> "List[T]":
        self.__list.append(item)
        return self

    def remove(self, item: T) -> "List[T]":
        self.__list.remove(item)
        return self

    def take(self, count: int) -> "List[T]":
        return List(self.__list[:count])

    def clear(self) -> None:
        self.__list.clear()

    def index_of(self, item: T) -> int:
        return self.__list.index(item)

    def map(self, func: Callable[[T], TOut]) -> "List[TOut]":
        return List(func(x) for x in self.__list)

    def reduce(self, func: Callable[[T, T], T]) -> T | None:
        if len(self.__list) == 0:
            return None

        accumulate = self.__list[0]
        for item in self.__list[1:]:
            accumulate = func(accumulate, item)

        return accumulate

    def filter(self, predicate: Callable[[T], bool]) -> "List[T]":
        return List(x for x in self.__list if predicate(x))

    def order(self, key_selector: Callable[[T], Any]) -> "List[T]":
        return List(sorted(self.__list, key=key_selector))

    def to_py_list(self) -> list[T]:
        return [x for x in self.__list]

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> "List[T]": ...

    def __getitem__(self, index: int | slice) -> T | "List[T]":
        if isinstance(index, slice):
            return List(self.__list[index])
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
