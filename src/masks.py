import logging
import os

from src.decorators import log_with_logger

# from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logs_folder = os.path.join(project_root, "logs", f"{logger.name}.log")

file_handler = logging.FileHandler(logs_folder, "w")
logger.addHandler(file_handler)

logger_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(logger_formatter)


@log_with_logger(logger)
def get_mask_card_number(card_number: str) -> str:
    """ "Функция принимает на вход номер карты и возвращает ее маску."""
    trimmed_card_number = card_number.replace(" ", "")
    if not trimmed_card_number.isdigit() or len(trimmed_card_number) != 16:
        raise ValueError("Invalid card number")
    return f"{trimmed_card_number[:4]} {trimmed_card_number[4:6]}** **** {trimmed_card_number[-4:]}"


@log_with_logger(logger)
def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску."""
    trimmed_account = account_number.replace(" ", "")
    if not trimmed_account.isdigit() or len(trimmed_account) < 6:
        raise ValueError("Invalid account number")
    return f"**{trimmed_account[-4:]}"
