import os
from datetime import datetime

import pandas as pd
import pytest


@pytest.fixture
def current_date() -> str:
    return datetime.now().isoformat()


@pytest.fixture
def valid_operations_data_dict() -> list:
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
    ]


@pytest.fixture
def incorrect_csv_file() -> str:
    file_name = "incorrect_csv_file.csv"
    with open(file_name, "w") as file:
        file.write("incorrect file; content\n")
    return file_name


@pytest.fixture
def unexisted_csv_file() -> str:
    return "name.csv"


@pytest.fixture
def valid_csv_file() -> str:
    file_name = "valid_csv_file.csv"
    with open(file_name, "w") as file:
        file.write("id;name;age\n")
        file.write("11;Sam;23\n")
        file.write("12;Tom;32\n")
    return file_name


@pytest.fixture
def empty_csv_file() -> str:
    file_name = "empty_csv_file.csv"
    file = open(file_name, "w")
    file.close()
    return file_name


@pytest.fixture
def unexisted_excel_file() -> str:
    return "unexisted_excel_file.xlsx"


@pytest.fixture
def empty_excel_file() -> str:
    file_name = "empty_excel_file.xlsx"
    file = open(file_name, "w")
    file.close()
    return file_name


@pytest.fixture
def invalid_excel_file() -> str:
    file_name = "invalid_excel_file.xlsx"
    with open(file_name, "w") as file:
        file.write("invalid data\n")
    return file_name


@pytest.fixture
def valid_excel_file() -> str:
    file_name = "valid_excel_file.xlsx"
    data = {"id": [1, 2], "name": ["Sam", "Tom"], "age": [23, 32]}
    df = pd.DataFrame(data)
    df.set_index("id", inplace=True)
    df.to_excel(file_name, index=True)
    return file_name


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_files():
    yield
    test_files = [
        "incorrect_csv_file.csv",
        "tmp.log",
        "empty_csv_file.csv",
        "valid_csv_file.csv",
        "valid_excel_file.xlsx",
        "empty_excel_file.xlsx",
        "invalid_excel_file.xlsx",
    ]
    for test_file in test_files:
        if os.path.exists(test_file):
            os.remove(test_file)
