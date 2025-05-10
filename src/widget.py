import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(score_info: str) -> str:
    """Функция принимает на вход строку формата 'Счет <score_number>' или '<Card> <card_number>'
    и возвращает маскированную строку"""
    score_info_split: list[str] = score_info.split()
    masked_info: str = ""

    if len(score_info_split) < 2:
        raise ValueError("Wrong  data.")

    if score_info_split[0] == "Счет" and len(score_info_split) == 2:
        masked_info = get_mask_account(score_info.split()[-1])
    elif score_info_split[0] != "Счет":
        masked_info = get_mask_card_number(score_info.split()[-1])
    else:
        raise ValueError("Wrong  data.")

    return f"{' '.join(score_info_split[:-1])} {masked_info}"


def get_date(date_string: str) -> str:
    """Функция принимает на вход строку с датой в формате iso 8601 и возвращает строку в формате '%d.%m.%Y'"""
    date_decoded = datetime.datetime.fromisoformat(date_string)

    return date_decoded.strftime("%d.%m.%Y")
