import datetime
from typing import Iterable


def filter_by_state(list: Iterable[dict], state: str = "EXECUTED") -> Iterable[dict]:
    """Фильтрация входящего списка словарей list по полю state"""
    return [item for item in list if item.get("state") == state]


def sort_by_date(list: Iterable[dict], reverse: bool = True) -> Iterable[dict]:
    """Сортировка входящего списка словапрей list по полю date, в возрастающем или убывающем порядке"""
    return sorted(list, key=lambda item: datetime.datetime.fromisoformat(item["date"]), reverse=reverse)
