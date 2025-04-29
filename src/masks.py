def get_mask_card_number(card_number: str) -> str:
    """ "Функция принимает на вход номер карты и возвращает ее маску."""
    trimmed_card_number = card_number.replace(" ", "")
    if not trimmed_card_number.isdigit() or len(trimmed_card_number) != 16:
        raise ValueError("Invalid card number")
    return f"{trimmed_card_number[:4]} {trimmed_card_number[4:6]}** **** {trimmed_card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску."""
    trimmed_account = account_number.replace(" ", "")
    if not trimmed_account.isdigit() or len(trimmed_account) < 6:
        raise ValueError("Invalid account number")
    return f"**{trimmed_account[-4:]}"
