import os
from unittest.mock import patch

from dotenv import load_dotenv

from src.external_api import get_converted_amount


@patch("requests.get")
def test_get_converted_amount(mock_get) -> None:
    load_dotenv()
    api_key = os.getenv("APILAYER_API_KEY")
    mock_get.return_value.json.return_value = {"result": 655238.782346}
    result = get_converted_amount("USD", 8221.37)
    headers = {"apikey": api_key}
    params = {"from": "USD", "to": "RUB", "amount": 8221.37}
    assert result == 655238.782346

    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert", headers=headers, params=params
    )
