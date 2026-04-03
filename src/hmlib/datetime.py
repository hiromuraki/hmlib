from __future__ import annotations
import time
from typing import Optional
from datetime import datetime


class DateTime:
    def __init__(self, unix_timestamp: float) -> None:
        if isinstance(unix_timestamp, float):
            self.__unix_timestamp = unix_timestamp
        else:
            raise ValueError("timestamp must be a float")

    @staticmethod
    def from_datetime(
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
        millisecond: Optional[int] = None,
    ) -> DateTime:
        """
        从日期时间组件创建DateTime对象

        Args:
            year: 年 (默认: 1970)
            month: 月 (默认: 1)
            day: 日 (默认: 1)
            hour: 时 (默认: 0)
            minute: 分 (默认: 0)
            second: 秒 (默认: 0)
            millisecond: 毫秒 (默认: 0)

        Returns:
            DateTime对象

        Raises:
            ValueError: 如果日期时间参数无效
        """
        # 设置默认值
        year = year if year is not None else 1970
        month = month if month is not None else 1
        day = day if day is not None else 1
        hour = hour if hour is not None else 0
        minute = minute if minute is not None else 0
        second = second if second is not None else 0
        millisecond = millisecond if millisecond is not None else 0

        # 验证参数范围
        if not (1 <= month <= 12):
            raise ValueError("month must be between 1 and 12")
        if not (1 <= day <= 31):
            raise ValueError("day must be between 1 and 31")
        if not (0 <= hour <= 23):
            raise ValueError("hour must be between 0 and 23")
        if not (0 <= minute <= 59):
            raise ValueError("minute must be between 0 and 59")
        if not (0 <= second <= 59):
            raise ValueError("second must be between 0 and 59")
        if not (0 <= millisecond <= 999):
            raise ValueError("millisecond must be between 0 and 999")

        try:
            dt = datetime(year, month, day, hour, minute, second, millisecond * 1000)
            unix_timestamp = dt.timestamp()
            return DateTime(unix_timestamp)
        except ValueError as e:
            raise ValueError(f"Invalid datetime parameters: {e}")

    @staticmethod
    def now() -> DateTime:
        return DateTime(time.time())

    @property
    def unix_timestamp(self) -> float:
        return self.__unix_timestamp

    @property
    def year(self) -> int:
        return time.localtime(self.__unix_timestamp).tm_year

    @property
    def month(self) -> int:
        return time.localtime(self.__unix_timestamp).tm_mon

    @property
    def day(self) -> int:
        return time.localtime(self.__unix_timestamp).tm_mday

    @property
    def hour(self) -> int:
        return time.localtime(self.__unix_timestamp).tm_hour

    @property
    def minute(self) -> int:
        return time.localtime(self.__unix_timestamp).tm_min

    @property
    def second(self) -> int:
        return time.localtime(self.__unix_timestamp).tm_sec

    def __hash__(self) -> int:
        return (int)(self.__unix_timestamp)

    def __str__(self) -> str:
        return time.strftime(
            r"%Y-%m-%d %H:%M:%S", time.localtime(self.__unix_timestamp)
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, value: DateTime) -> bool:
        return self.__unix_timestamp == value.__unix_timestamp

    def __gt__(self, __o: DateTime) -> bool:
        return self.__unix_timestamp > __o.__unix_timestamp

    def __lt__(self, __o: DateTime) -> bool:
        return self.__unix_timestamp < __o.__unix_timestamp
