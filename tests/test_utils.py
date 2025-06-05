import csv
import json
from unittest import mock
from unittest.mock import patch

import pytest

from src.utils import get_transaction_ammount, read_csv_data, read_exel_data, read_transactions_data


def test_read_transactions_data_invalid_file_path() -> None:
    assert read_transactions_data("filename") == []


def test_read_transactions_data_invalid_json() -> None:
    read_data = "invalid json"
    mocked_open = mock.mock_open(read_data=read_data)
    with patch("builtins.open", mocked_open):
        result = read_transactions_data("filename")
    assert result == []


def test_read_transactions_data_valid_data(valid_operations_data_dict: list) -> None:
    read_data = json.dumps(valid_operations_data_dict)
    mocked_open = mock.mock_open(read_data=read_data)
    with patch("builtins.open", mocked_open):
        result = read_transactions_data("filename")
    assert len(result) == 2
    assert result[0]["id"] == 441945886
    assert result[1]["id"] == 41428829


@mock.patch("src.utils.get_converted_amount")
def test_get_transaction_amount_api_call(mock_get) -> None:
    data = {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    }
    mock_get.return_value = 655238.782346
    result = get_transaction_ammount(data)
    assert result == 655238.782346
    mock_get.assert_called_once_with("USD", 8221.37)


@mock.patch("src.utils.get_converted_amount")
def test_get_transaction_amount_api_do_not_called(mock_get) -> None:
    data = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    }
    result = get_transaction_ammount(data)
    assert result == 31957.58
    mock_get.assert_not_called()


@pytest.mark.parametrize(
    "input, output", [("unexisted_csv_file", []), ("incorrect_csv_file", []), ("empty_csv_file", [])]
)
def test_read_odd_csv_data(input, output, request):
    file_name = request.getfixturevalue(input)
    assert read_csv_data(file_name) == output


@pytest.mark.parametrize(
    "input, output",
    [
        ("valid_csv_file", [["id", "name", "age"], ["11", "Sam", "23"], ["12", "Tom", "32"]]),
    ],
)
def test_read_valid_csv_data(input, output, request):
    file_name = request.getfixturevalue(input)
    with open(file_name) as f:
        reader = csv.reader(f, delimiter=";")
        assert next(reader) == output[0]
        assert next(reader) == output[1]
        assert next(reader) == output[2]


@pytest.mark.parametrize(
    "input, output", [("unexisted_excel_file", []), ("empty_excel_file", []), ("invalid_excel_file", [])]
)
def test_read_excel_odd_data(input, output, request):
    file_name = request.getfixturevalue(input)
    data = read_exel_data(file_name)
    assert data == []


@pytest.mark.parametrize(
    "input, output",
    [
        ("valid_excel_file", [1, 2]),
    ],
)
def test_read_excel_valid_data(input, output, request):
    file_name = request.getfixturevalue(input)
    data = read_exel_data(file_name)
    assert data[0]["id"] == output[0]
    assert data[1]["id"] == output[1]
