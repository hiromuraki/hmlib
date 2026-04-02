from typing import Any


class DynamicObject:
    def __init__(self, obj: Any) -> None:
        self.__obj = obj

    def int(self) -> int:
        if type(self.__obj) is not int:
            raise ValueError()

        return self.__obj

    def float(self) -> float:
        if type(self.__obj) is not float:
            raise ValueError()

        return self.__obj

    def str(self) -> str:
        if type(self.__obj) is not str:
            raise ValueError()

        return self.__obj

    def bool(self) -> bool:
        if type(self.__obj) is not bool:
            raise ValueError()

        return self.__obj

    def is_none(self) -> "bool":
        return self.__obj is None

    def __str__(self) -> "str":
        return str(self.__obj)

    def __getattr__(self, property: "str") -> "DynamicObject":
        if self.__obj is None:
            return DynamicObject(None)

        if hasattr(self.__obj, "get"):
            return DynamicObject(self.__obj.get(property))
        return DynamicObject(None)
