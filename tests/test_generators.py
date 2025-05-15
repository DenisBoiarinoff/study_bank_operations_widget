from typing import Iterable, List

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    number_to_string_convertion,
    transaction_descriptions,
)


@pytest.mark.parametrize(
    "input, currency_code, output_ids",
    [
        (
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
                {
                    "id": 142264268,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                },
                {
                    "id": 873106923,
                    "state": "EXECUTED",
                    "date": "2019-03-23T01:09:46.296404",
                    "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 44812258784861134719",
                    "to": "Счет 74489636417521191160",
                },
                {
                    "id": 895315941,
                    "state": "EXECUTED",
                    "date": "2018-08-19T04:27:37.904916",
                    "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод с карты на карту",
                    "from": "Visa Classic 6831982476737658",
                    "to": "Visa Platinum 8990922113665229",
                },
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                    "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод организации",
                    "from": "Visa Platinum 1246377376343588",
                    "to": "Счет 14211924144426031657",
                },
            ],
            "USD",
            [939719570, 142264268, 895315941],
        ),
    ],
)
def test_filter_by_currency_correct_data(input: dict, currency_code: str, output_ids: Iterable[int]) -> None:
    generator = filter_by_currency(input, currency_code)
    for id in output_ids:
        assert id == next(generator)["id"]

    with pytest.raises(StopIteration):
        next(generator)


@pytest.mark.parametrize(
    "input, currency_code",
    [
        (
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
                {
                    "id": 142264268,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                },
                {
                    "id": 873106923,
                    "state": "EXECUTED",
                    "date": "2019-03-23T01:09:46.296404",
                    "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 44812258784861134719",
                    "to": "Счет 74489636417521191160",
                },
                {
                    "id": 895315941,
                    "state": "EXECUTED",
                    "date": "2018-08-19T04:27:37.904916",
                    "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод с карты на карту",
                    "from": "Visa Classic 6831982476737658",
                    "to": "Visa Platinum 8990922113665229",
                },
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                    "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод организации",
                    "from": "Visa Platinum 1246377376343588",
                    "to": "Счет 14211924144426031657",
                },
            ],
            "123",
        ),
        ([], "USD"),
    ],
)
def test_filter_by_currency_absent_code(input: dict, currency_code: str) -> None:
    generator = filter_by_currency(input, currency_code)
    with pytest.raises(StopIteration):
        next(generator)


@pytest.mark.parametrize(
    "input, output",
    [
        (1, "0000000000000001"),
        (10, "0000000000000010"),
        (100, "0000000000000100"),
        (1000, "0000000000001000"),
        (8888, "0000000000008888"),
        (0, "0000000000000001"),
        (10000, "0000000000010000"),
        (1000000000000000, "1000000000000000"),
    ],
)
def test_number_to_string_convertion(input: int, output: str) -> None:
    assert number_to_string_convertion(input) == output


@pytest.mark.parametrize("initial, results", [((99990000, 99999999), ["0000 0000 9999 0000", "0000 0000 9999 0001"])])
def test_card_number_generator_valid_data(initial: List[int], results: str) -> None:
    generator = card_number_generator(initial[0], initial[1])
    for result in results:
        assert next(generator) == result


@pytest.mark.parametrize("initial, results", [((9999, 10000), ["0000 0000 0000 9999", "0000 0000 0001 0000"])])
def test_card_number_generator_edges(initial: List[int], results: str) -> None:
    generator = card_number_generator(initial[0], initial[1])
    for result in results:
        assert next(generator) == result

    with pytest.raises(StopIteration):
        next(generator)


@pytest.mark.parametrize(
    "input, output",
    [
        (
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
                {
                    "id": 142264268,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                },
                {
                    "id": 873106923,
                    "state": "EXECUTED",
                    "date": "2019-03-23T01:09:46.296404",
                    "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 44812258784861134719",
                    "to": "Счет 74489636417521191160",
                },
                {
                    "id": 895315941,
                    "state": "EXECUTED",
                    "date": "2018-08-19T04:27:37.904916",
                    "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод с карты на карту",
                    "from": "Visa Classic 6831982476737658",
                    "to": "Visa Platinum 8990922113665229",
                },
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                    "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод организации",
                    "from": "Visa Platinum 1246377376343588",
                    "to": "Счет 14211924144426031657",
                },
            ],
            [
                "Перевод организации",
                "Перевод со счета на счет",
                "Перевод со счета на счет",
                "Перевод с карты на карту",
                "Перевод организации",
            ],
        ),
    ],
)
def test_transaction_descriptions_correct_data(input: Iterable[dict], output: Iterable[str]) -> None:
    generator = transaction_descriptions(input)
    for description in output:
        assert description == next(generator)

    with pytest.raises(StopIteration):
        next(generator)


@pytest.mark.parametrize(
    "input",
    ([]),
)
def test_transaction_descriptions_empty_data(input: Iterable[dict]) -> None:
    generator = transaction_descriptions(input)

    with pytest.raises(StopIteration):
        next(generator)


@pytest.mark.parametrize(
    "input",
    (
        [
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
                "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
                "from": "Visa Platinum 1246377376343588",
                "to": "Счет 14211924144426031657",
            }
        ],
        [
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
                "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
                "description_1": "Перевод организации",
                "from": "Visa Platinum 1246377376343588",
                "to": "Счет 14211924144426031657",
            }
        ],
    ),
)
def test_transaction_descriptions_incorrect_data(input: Iterable[dict]) -> None:
    generator = transaction_descriptions(input)

    assert next(generator) is None

    with pytest.raises(StopIteration):
        next(generator)
