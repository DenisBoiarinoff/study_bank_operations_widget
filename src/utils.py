import json
from typing import List

from src.external_api import get_converted_amount


def read_transactions_data(filename: str) -> List[dict]:
    """Читает данные из .json файла имя которого переданно в качестве параметра"""
    data = []
    try:
        with open(filename) as file:
            data = json.load(file)
    except Exception:
        pass
    return data


def get_transaction_ammount(transaction: dict) -> float:
    """Возвращает стоймость транзакции в рублях, в случае если валюта транзакции не
    рубли переводит сумму по текущему курсу"""
    transaction_amount = transaction["operationAmount"]
    transaction_concurrency_code = transaction_amount["currency"]["code"]
    transaction_concurrency_amount = float(transaction_amount["amount"])
    if transaction_concurrency_code == "RUB":
        return transaction_concurrency_amount
    else:
        return get_converted_amount(transaction_concurrency_code, transaction_concurrency_amount)
