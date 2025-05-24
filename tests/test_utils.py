import json
from unittest import mock
from unittest.mock import patch

from src.utils import get_transaction_ammount, read_transactions_data


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
