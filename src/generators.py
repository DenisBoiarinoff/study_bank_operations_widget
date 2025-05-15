from typing import Any, Generator, Iterable


def filter_by_currency(transactions: Iterable[dict], currency_code: str) -> Generator[dict]:
    """Функция принимает список словарей транзакций и код валюты,
    возвращает генератор по отфильтрованному по валюте списку"""
    return (info for info in transactions if info["operationAmount"]["currency"]["code"] == currency_code)


def transaction_descriptions(transactions: Iterable[dict]) -> Generator[Any | None]:
    """Функция принимает список словарей транщакций а врзврашает генератор по списку полей description транзакций"""
    return (info.get("description") for info in transactions)


def number_to_string_convertion(number: int) -> str:
    """Преобразует число от 1 до 9999999999999999 в строку формата XXXXXXXXXXXXXXXXX,
    дополняя смволпом '0' недостающие разряды."""
    normalized_number = min(9999999999999999, max(number, 1))
    power = 16
    for index in range(16):
        if normalized_number % 10**index == normalized_number:
            power = index
            break
    return f"{"0" * (16 - power)}{normalized_number}"


def card_number_generator(lower: int, upper: int) -> Generator[str]:
    """Функция принимает границы интервала и врзвращает генератор номеров каот в указанных границах"""
    for index in range(max(lower, 1), min(upper + 1, 9999999999999999)):
        number_string = number_to_string_convertion(index)
        splited_number = [number_string[i : i + 4] for i in range(0, 16, 4)]
        yield " ".join(splited_number)
