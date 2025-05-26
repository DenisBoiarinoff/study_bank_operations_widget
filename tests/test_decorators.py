import logging
import os

import pytest

from src.decorators import log, log_with_logger

test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("tmp.log", "w")
test_logger.addHandler(file_handler)

logger_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(logger_formatter)


@log()
def console_decorated_console_function(x, y):
    return x + y


@log("tmp.txt")
def console_decorated_file_function(x, y):
    return x + y


@log_with_logger(test_logger)
def logger_decorated_function(x, y):
    return x + y


@pytest.mark.parametrize(
    "first, second",
    [
        (1, [1]),
        (1, (1,)),
        (1, "1"),
    ],
)
def test_decorator_error(first, second):
    with pytest.raises(TypeError):
        console_decorated_console_function(first, second)


@pytest.mark.parametrize(
    "first, second, console_output",
    [
        (1, 1, "\nconsole_decorated_console_function ok\n\n"),
        ("1", "1", "\nconsole_decorated_console_function ok\n\n"),
        (True, True, "\nconsole_decorated_console_function ok\n\n"),
    ],
)
def test_decorator_success_console_output(capsys, first, second, console_output):
    console_decorated_console_function(first, second)
    captured = capsys.readouterr()
    assert captured.out == console_output


@pytest.mark.parametrize(
    "first, second, console_output",
    [
        (1, [1], "\nconsole_decorated_console_function error: TypeError. Inputs: (1, [1]), {}\n\n"),
        (1, (1,), "\nconsole_decorated_console_function error: TypeError. Inputs: (1, (1,)), {}\n\n"),
        (1, "1", "\nconsole_decorated_console_function error: TypeError. Inputs: (1, '1'), {}\n\n"),
    ],
)
def test_decorator_error_console_output(capsys, first, second, console_output):
    try:
        console_decorated_console_function(first, second)
    except Exception:
        captured = capsys.readouterr()
        assert captured.out == console_output


@pytest.mark.parametrize(
    "first, second, file_string",
    [
        (1, [1], "console_decorated_file_function error: TypeError. Inputs: (1, [1]), {}\n"),
        (1, (1,), "console_decorated_file_function error: TypeError. Inputs: (1, (1,)), {}\n"),
        (1, "1", "console_decorated_file_function error: TypeError. Inputs: (1, '1'), {}\n"),
    ],
)
def test_decorator_error_file_output(first, second, file_string):
    try:
        console_decorated_file_function(first, second)
    except Exception:
        with open("tmp.txt", "r") as file:
            lines = file.readlines()
            assert len(lines) == 2
            assert lines[1] == file_string
    else:
        assert False
    finally:
        os.remove("tmp.txt")


@pytest.mark.parametrize(
    "first, second, file_string",
    [
        (1, 1, "console_decorated_file_function ok\n"),
        ("1", "1", "console_decorated_file_function ok\n"),
        (True, True, "console_decorated_file_function ok\n"),
    ],
)
def test_decorator_success_file_output(first, second, file_string):
    try:
        console_decorated_file_function(first, second)
    except Exception:
        assert False
    else:
        with open("tmp.txt", "r") as file:
            lines = file.readlines()
            assert len(lines) == 2
            assert lines[1] == file_string
    finally:
        os.remove("tmp.txt")


@pytest.mark.parametrize(
    "first, second, log_strings",
    [
        (
            1,
            1,
            [
                "test_logger INFO: Will start logger_decorated_function\n",
                "test_logger INFO: Will return 2\n",
            ],
        ),
        ("1", "1", ["test_logger INFO: Will start logger_decorated_function\n", "test_logger INFO: Will return 11\n"]),
        (
            True,
            True,
            ["test_logger INFO: Will start logger_decorated_function\n", "test_logger INFO: Will return 2\n"],
        ),
    ],
)
def test_log_with_logger_decorator_valid_data(first, second, log_strings):
    try:
        logger_decorated_function(first, second)
    except Exception:
        assert False
    else:
        with open("tmp.log", "r") as file:
            lines = file.readlines()
            for index, string in enumerate(log_strings):
                assert string in lines[-(len(log_strings) - index)]


@pytest.mark.parametrize(
    "first, second, log_strings",
    [
        (
            1,
            [1],
            [
                "test_logger INFO: Will start logger_decorated_function\n",
                "test_logger ERROR: logger_decorated_function - TypeError. Inputs: (1, [1]), {}\n",
            ],
        ),
        (
            1,
            (1,),
            [
                "test_logger INFO: Will start logger_decorated_function\n",
                "test_logger ERROR: logger_decorated_function - TypeError. Inputs: (1, (1,)), {}\n",
            ],
        ),
        (
            1,
            "1",
            [
                "test_logger INFO: Will start logger_decorated_function\n",
                "test_logger ERROR: logger_decorated_function - TypeError. Inputs: (1, '1'), {}\n",
            ],
        ),
    ],
)
def test_log_with_logger_decorator_invalid_data(first, second, log_strings):
    try:
        logger_decorated_function(first, second)
    except Exception:
        with open("tmp.log", "r") as file:
            lines = file.readlines()
            for index, string in enumerate(log_strings):
                assert string in lines[-(len(log_strings) - index)]
    else:
        assert False
