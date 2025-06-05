from src.processing import filter_by_rub, filter_by_state, find_by_description, sort_by_date
from src.utils import read_csv_data, read_exel_data, read_transactions_data
from src.widget import get_date, mask_account_card


def ask_for_data_source(processing_settings: dict) -> dict:
    """Получить от пользователя источник данных"""
    print("Выберите необходимый пункт меню:\n")
    print("1. Получить информацию о транзакциях из JSON-файла\n")
    print("2. Получить информацию о транзакциях из CSV-файла\n")
    print("3. Получить информацию о транзакциях из XLSX-файла\n")
    user_answer = 0
    while user_answer not in ["1", "2", "3"]:
        user_answer = input("Пользователь: ").strip()

    message = ""
    if user_answer == "1":
        message = "Программа: Для обработки выбран JSON-файл."
    elif user_answer == "2":
        message = "Программа: Для обработки выбран CSV-файл."
    else:
        message = "Программа: Для обработки выбран XLSX-файл."
    print(message)

    processing_settings["data_source"] = int(user_answer)

    return processing_settings


def sak_for_operations_status(processing_settings: dict) -> dict:
    """Получение от пользователя статус интересующих его операций"""
    operations_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    user_answer = ""
    while user_answer not in operations_statuses:
        if user_answer != "":
            print(f'Программа: Статус операции "{user_answer}" недоступен.\n\n')

        if user_answer.upper() not in operations_statuses:
            print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n")
            print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n")

        user_answer = input("Пользователь: ").strip()

    user_answer = user_answer.upper()
    print(f'Программа: Операции отфильтрованы по статусу "{user_answer}"')

    processing_settings["operations_status"] = user_answer

    return processing_settings


def ask_for_date_sort_option(processing_settings: dict) -> dict:
    """Получиение от польщователя опции сортировки по дате"""
    valid_answers = ["ДА", "НЕТ"]

    user_answer = ""
    while user_answer.upper() not in valid_answers:
        print("Программа: Отсортировать операции по дате? Да/Нет\n")
        user_answer = input("Пользователь: ").strip()

    user_answer = user_answer.upper()

    processing_settings["date_sort_option"] = user_answer == valid_answers[0]

    return processing_settings


def ask_for_asc_desc_sort_option(processing_settings: dict) -> dict:
    """Получение от пользователя опции сортировки по аозрастанию/убыванию"""
    valid_answers = ["ПО ВОЗРАСТАНИЮ", "ПО УБЫВАНИЮ"]

    user_answer = ""
    while user_answer.upper() not in valid_answers:
        print("Программа: Отсортировать по возрастанию или по убыванию?\n")
        user_answer = input("Пользователь: ").strip()

    user_answer = user_answer.upper()

    processing_settings["asc_sort_option"] = user_answer == valid_answers[1]

    return processing_settings


def ask_for_rub_filter(processing_settings: dict) -> dict:
    """Получение от пользщователя опции фильтрации по рублёвым операциям"""
    valid_answers = ["ДА", "НЕТ"]

    user_answer = ""
    while user_answer.upper() not in valid_answers:
        print("Программа: Выводить только рублевые транзакции? Да/Нет\n")
        user_answer = input("Пользователь: ").strip()

    user_answer = user_answer.upper()

    processing_settings["rub_filter"] = user_answer == valid_answers[0]

    return processing_settings


def ask_for_description_filter(processing_settings: dict) -> dict:
    """Получение от рользователя опции фильтрации по описанию"""
    valid_answers = ["ДА", "НЕТ"]

    user_answer = ""
    while user_answer.upper() not in valid_answers:
        print("Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n")
        user_answer = input("Пользователь: ").strip()

    user_answer = user_answer.upper()

    processing_settings["description_filter"] = user_answer == valid_answers[0]

    if user_answer == valid_answers[0]:
        print("Программа: Введите слово для фильтрации")
        filter_word = ""
        while len(filter_word.strip()) == 0:
            filter_word =  input("Пользователь: ")
            processing_settings["filter_word"] = filter_word

    return processing_settings


def execute_processing(processing_settings: dict) -> None:
    """Обработка данных согласено выбранным настройкам"""
    file_path = ""
    operations_data = {}
    data_source = processing_settings.get("data_source", 1)
    if data_source == 1:
        file_path = "./data/operations.json"
        operations_data = read_transactions_data(file_path)
    elif data_source == 2:
        file_path = "./data/transactions.csv"
        operations_data = read_csv_data(file_path)
    else:
        file_path = "./data/transactions_excel.xlsx"
        operations_data = read_exel_data(file_path)

    operations_status = processing_settings.get("operations_status", "EXECUTED")
    operations_data = filter_by_state(operations_data, operations_status)

    if processing_settings.get("date_sort_option", True):
        is_asc = processing_settings.get("asc_sort_option", True)
        operations_data = sort_by_date(operations_data, reverse=is_asc is True)

    if processing_settings.get("rub_filter", True):
        operations_data = filter_by_rub(operations_data)

    if processing_settings.get("description_filter", True):
        operations_data = find_by_description(operations_data, processing_settings.get("filter_word", ""))

    print_processing_result(operations_data)


def print_processing_result(operations: list[dict]) -> None:
    """Выводит результат обработкм данных на экран"""

    if len(operations) == 0:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

    print("Программа: Распечатываю итоговый список транзакций...\n")
    print(f"Программа: Всего банковских операций в выборке: {len(operations)}\n")

    for operation in operations:
        print(f"{get_date(operation.get("date"))} {operation.get("description")}\n")

        money_source = operation.get("from")
        if money_source is not None:
            print(f"{mask_account_card(money_source)}\n")

        amount = operation.get("operationAmount")
        if amount is not None:
            print(f"Сумма: {amount.get("amount")} {amount.get("currency").get("name")}")


def main() -> None:
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n")
    program_settings = {}

    program_settings = ask_for_data_source(program_settings)
    program_settings = sak_for_operations_status(program_settings)
    program_settings = ask_for_date_sort_option(program_settings)
    program_settings = ask_for_asc_desc_sort_option(program_settings)
    program_settings = ask_for_rub_filter(program_settings)
    program_settings = ask_for_description_filter(program_settings)
    execute_processing(program_settings)