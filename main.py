from src.data_readers import read_csv_data, read_exel_data
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.utils import get_transaction_ammount, read_transactions_data
from src.widget import get_date, mask_account_card

if __name__ == "__main__":
    print("Main start")
    print(get_mask_card_number("7000792289606361"))
    try:
        print(get_mask_card_number("361"))
    except Exception:
        pass
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Maestro 7000792289606361"))
    print(get_date("2024-03-11T02:26:18.671407"))
    print(
        filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    )
    print(
        filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "CANCELED",
        )
    )
    print(
        sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    )
    print(
        sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            reverse=False,
        )
    )
    print("------------------------------------------------------------")
    print(read_transactions_data("./data/operations.json"))
    print(read_transactions_data("./data/operations1.json"))
    print(read_transactions_data("./data/test.json"))
    print("-------------------------------------------------------------")
    operations_data = read_transactions_data("./data/operations.json")
    print(get_transaction_ammount(operations_data[0]))
    print(get_transaction_ammount(operations_data[1]))
    print("-------------------------------------------------------------")
    csv_data = read_csv_data("./data/transactions.csv")
    print(csv_data[:5])
    exel_data = read_exel_data("./data/transactions_excel.xlsx")
    print(exel_data[:5])
