from src.processing import filter_by_state, sort_by_date
import pytest

@pytest.mark.parametrize(
    "input, output",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            [
                {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
            ]
        ),
        (
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            []
        ),
        ([], []),
    ]
)
def test_filter_by_state_expected_data(input, output):
    assert filter_by_state(input) == output


@pytest.mark.parametrize(
    "input, state, output",
    [
        (
                [
                    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                ],
                "EXECUTED",
                [
                    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
                ]
        ),
        (
                [
                    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                ],
                "CANCELED",
                [
                    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                ]
        ),
    ]
)
def test_filter_by_state_with_state_data(input, state, output):
    assert filter_by_state(input, state=state) == output


@pytest.mark.parametrize(
    "input, output",
    [
        (
                [
                    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                ],
                [
                    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
                    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
                ]
        ),
    ]
)
def test_sort_by_date_no_sort_order_data(input, output):
    assert sort_by_date(input) == output


@pytest.mark.parametrize(
    "input, output",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 594226727, "state": "CANCELED", "date": "2019-07-03T18:35:29.512364"},
            ],
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 594226727, "state": "CANCELED", "date": "2019-07-03T18:35:29.512364"},
            ]
        ),
    ]
)
def test_sort_by_date_same_date(input, output):
    assert sort_by_date(input) == output


@pytest.mark.parametrize(
    "input, reverse, output",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            True,
            [
                {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
                {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
            ]
        ),
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            False,
            [
                {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
                {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
            ]
        ),
        ( [], True, [] ),
        ( [], False, [] ),
    ]
)
def test_sort_by_date_expected_data(input, reverse, output):
    assert sort_by_date(input, reverse=reverse) == output


@pytest.mark.parametrize(
    "input, output",
    [
        (
                [
                    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03"},
                    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58"},
                    {"id": 594226727, "state": "CANCELED", "date": "2021-09-12T21:27:25.241689"},
                    {"id": 615064591, "state": "CANCELED", "date": "2020-10-14T08:21"},
                ],
                [
                    {"id": 594226727, "state": "CANCELED", "date": "2021-09-12T21:27:25.241689"},
                    {"id": 615064591, "state": "CANCELED", "date": "2020-10-14T08:21"},
                    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03"},
                    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58'},
                ]
        ),
    ]
)
def test_sort_by_date_different_date_format(input, output):
    assert sort_by_date(input) == output


@pytest.mark.parametrize(
    "input",
    [
        ( [ {"id": 41428829, "state": "EXECUTED", "date": 123}, ] ),
        ( [ {"id": 939719570, "state": "EXECUTED", "date": True}, ] ),
        ( [ {"id": 594226727, "state": "CANCELED", "date": 1.0}, ] ),
        ( [ {"id": 615064591, "state": "CANCELED", "date": [ "2018-06-30T02:08:58" ] }, ] ),
    ]
)
def test_sort_by_date_wrong_date_format(input):
    with pytest.raises(TypeError) as exc_info:
        sort_by_date(input)


@pytest.mark.parametrize(
    "input",
    [
        ( [ {"id": 594226727, "state": "CANCELED", "date": "2021-20-12T21:27:25.241689"} ] ),
        ( [ {"id": 594226727, "state": "CANCELED", "date": "2021-001-12T21:27:25.241689"} ] ),
        ( [ {"id": 594226727, "state": "CANCELED", "date": "-0001-001-12T21:27:25.241689"} ] ),
        ( [ {"id": 594226727, "state": "CANCELED", "date": "2021-01-12T26:27:25.241689"} ] ),
        ( [ {"id": 594226727, "state": "CANCELED", "date": "2021-01-12T21:70:25.241689"} ] ),
        ( [ {"id": 594226727, "state": "CANCELED", "date": "2021-01-12T26:27:70.241689"} ] ),
        ( [ {"id": 594226727, "state": "CANCELED", "date": "2021-01-12T26:27:25.2416896546754"} ] ),
    ]
)
def test_sort_by_date_odd_date_format(input):
    with pytest.raises(ValueError) as exc_info:
        sort_by_date(input)