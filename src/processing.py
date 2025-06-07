import datetime
import re
from collections import Counter
from typing import Iterable


def filter_by_state(operations: Iterable[dict], state: str = "EXECUTED") -> Iterable[dict]:
    """Фильтрация входящего списка словарей operations по полю state"""
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: Iterable[dict], reverse: bool = True) -> Iterable[dict]:
    """Сортировка входящего списка словапрей operations по полю date, в возрастающем или убывающем порядке"""
    return sorted(
        operations, key=lambda operation: datetime.datetime.fromisoformat(operation["date"]), reverse=reverse
    )


def find_by_description(operations: list[dict], search_string: str) -> list[dict]:
    """Фильтрация входящего списка словарей operations по наличию в поле description подстроки search_string"""
    return list(
        filter(
            lambda operation: re.search(search_string, operation.get("description", ""), flags=re.IGNORECASE)
            is not None,
            operations,
        )
    )


def group_operations_by_transaction(operations: list[dict], operation_categories: list[str]) -> dict:
    """Возвращает счетчик по типам операций, переданных в параметре operation_categories, из списка operations"""
    return Counter(
        [
            operation["description"]
            for operation in operations
            if operation.get("description", "") in operation_categories
        ]
    )


def filter_by_rub(operations: list[dict]) -> list[dict]:
    """Фильтрация входящего списка транзакций operations по полю валюте RUB"""
    return [
        operation for operation in operations if operation.get("operationAmount").get("currency").get("code") == "RUB"
    ]
