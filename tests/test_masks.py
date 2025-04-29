import pytest

from src.masks import get_mask_card_number, get_mask_account
from tests.conftest import odd_card_numbers


@pytest.mark.parametrize(
    "card_number, mask",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("3500192289606821", "3500 19** **** 6821"),
    ]
)
def test_get_mask_card_number_expected_data(card_number, mask):
    assert get_mask_card_number(card_number) == mask

@pytest.mark.parametrize(
    "card_number",
    [
        ("11111111"),
        ("111111111111111111"),
        (""),
        ("                "),
        ("aaaaaaaaaaaaaaaa"),
        ("1111aaaa    1111"),
        ("11112222    1111"),
        ("11112222cccc3333"),
    ]
)
def test_get_mask_card_number_odd_data(card_number):
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(card_number)


@pytest.mark.parametrize(
    "card_number, mask",
    [
        ("   7000792289606361", "7000 79** **** 6361"),
        ("7000 7922 8960 6361", "7000 79** **** 6361"),
        ("7000792289606361    ", "7000 79** **** 6361"),
    ]
)
def test_get_mask_card_number_odd_valid_data(card_number, mask):
    assert get_mask_card_number(card_number) == mask

@pytest.mark.parametrize(
    "account, mask",
    [
        ("73654108430135874305", "**4305"),
        ("34584323423545456535", "**6535"),
    ]
)
def test_get_mask_account_expected_data(account, mask):
    assert get_mask_account(account) == mask


@pytest.mark.parametrize(
    "account",
    [
        ("asdsdfdsdfdsdfdsdfv"),
        ("       "),
        (""),
        ("-1"),
    ]
)
def test_get_mask_account_odd_data(account):
    with pytest.raises(ValueError) as exc_info:
        get_mask_account(account)


@pytest.mark.parametrize(
    "account, mask",
    [
        ("7365 4108 430135 874305", "**4305"),
        ("    73654108430135874305", "**4305"),
        ("73654108430135874305          ", "**4305"),
        ("123456", "**3456")
    ]
)
def test_get_mask_account_odd_valid_data(account, mask):
    assert get_mask_account(account) == mask