from datetime import datetime

import pytest

from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "input, output",
    [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361")
    ]
)
def test_mask_account_card_valid_data(input, output):
    assert mask_account_card(input) == output


@pytest.mark.parametrize(
    "input",
    [
        ("Visa Platinum 73654108430154354335874305"),
        ("Счет Visa Platinum 73654108430135874305"),
        ("Счет Visa Platinum 7000792289606361"),
        ("Счет"),
        ("Visa Platinum"),
        ("Maestro"),
        (""),
        ("          "),
        ("7000 7922 8960 6361"),
        ("73654108430154354335874305")
    ]
)
def test_mask_account_card_invalid_data(input):
    with pytest.raises(ValueError) as exc_info:
        mask_account_card(input)

@pytest.mark.parametrize(
    "input, output",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2019-07-03", "03.07.2019"),
        ("2018-06-30T02:08:58", "30.06.2018"),
        ("2021-09-12T21:27:25.241689", "12.09.2021"),
        ("2020-10-14T08:21", "14.10.2020")
    ]
)
def test_get_date_valid_data(input, output):
    assert get_date(input) == output


def test_get_date_current_date(current_date):
    assert get_date(current_date) == datetime.today().strftime('%d.%m.%Y')


@pytest.mark.parametrize(
    "input",
    [
        (""),
        ("     "),
        ("2021-20-12T21:27:25.241689"),
        ("2021-001-12T21:27:25.241689"),
        ("-0001-001-12T21:27:25.241689"),
        ("2021-01-12T26:27:25.241689"),
        ("2021-01-12T21:70:25.241689"),
        ("2021-01-12T26:27:70.241689"),
        ("2021-01-12T26:27:25.2416896546754"),
    ]
)
def test_get_date_invalid_data(input):
    with pytest.raises(ValueError) as exc_info:
        get_date(input)