import datetime
from typing import Union

MONTH_ALIASES = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12",
}


def get_datetime_lazy(
    day: Union[str, int], month: str, year: Union[str, int]
) -> datetime.datetime:
    instance = datetime.datetime(
        day=int(day), month=int(MONTH_ALIASES[month.strip()]), year=int(year)
    )
    return instance
