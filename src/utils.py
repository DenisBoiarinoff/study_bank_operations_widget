import json
import logging
import os
from typing import List

from src.decorators import log_with_logger
from src.external_api import get_converted_amount

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logs_folder = os.path.join(project_root, "logs", f"{logger.name}.log")

file_handler = logging.FileHandler(logs_folder, "w")
logger.addHandler(file_handler)

logger_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(logger_formatter)


@log_with_logger(logger)
def read_transactions_data(filename: str) -> List[dict]:
    """Читает данные из .json файла имя которого переданно в качестве параметра"""
    data = []
    try:
        with open(filename) as file:
            data = json.load(file)
    except Exception as e:
        logger.warning(f"Read data error {repr(e)}")
        pass
    return data


@log_with_logger(logger)
def get_transaction_ammount(transaction: dict) -> float:
    """Возвращает стоймость транзакции в рублях, в случае если валюта транзакции не
    рубли переводит сумму по текущему курсу"""
    transaction_amount = transaction["operationAmount"]
    transaction_concurrency_code = transaction_amount["currency"]["code"]
    transaction_concurrency_amount = float(transaction_amount["amount"])
    if transaction_concurrency_code == "RUB":
        return transaction_concurrency_amount
    else:
        logger.info("Will requesting external api")
        return get_converted_amount(transaction_concurrency_code, transaction_concurrency_amount)
