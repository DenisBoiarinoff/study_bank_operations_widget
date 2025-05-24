import os

import requests
from dotenv import load_dotenv


def get_converted_amount(from_concurrency_code: str, amount: float) -> any:
    """Получает текущий обменный курс переданной в качкстве параметра валюты к рублю"""
    load_dotenv()
    api_key = os.getenv("APILAYER_API_KEY")
    headers = {"apikey": api_key}
    params = {"from": from_concurrency_code, "to": "RUB", "amount": amount}
    exchange_rate = requests.get("https://api.apilayer.com/exchangerates_data/convert", headers=headers, params=params)
    return exchange_rate.json()["result"]
