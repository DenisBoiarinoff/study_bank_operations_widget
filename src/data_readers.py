from csv import DictReader

import pandas as pd


def read_csv_data(filename: str) -> list[dict]:
    """Возвращает список словарей с данными файла .csv имя которого передано в качестве параметра"""
    result = []
    try:
        with open(filename) as csv_file:
            reader = DictReader(csv_file, delimiter=";")
            result = list(reader)
    except Exception:
        pass
    return result


def read_exel_data(filename: str) -> list[dict]:
    """Возвращает список словарей с данными файла .xlsx имя которого передано в качестве параметра"""
    result = []
    try:
        excel_data = pd.read_excel(filename)
        result = excel_data.to_dict(orient="records")
    except Exception:
        pass
    return result
