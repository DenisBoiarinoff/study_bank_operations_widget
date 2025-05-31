import csv

import pytest

from src.data_readers import read_csv_data, read_exel_data


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
