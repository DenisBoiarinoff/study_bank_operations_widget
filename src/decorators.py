from functools import wraps
from typing import Optional


def write_result(message: str, filename: Optional[str] = None) -> None:
    """Записывает переданное сообщение в файл, если предано имя, или в консоль, в противном случае."""
    if filename is None:
        print(message)
    else:
        with open(filename, "w") as file:
            file.write(message)


def log(filename: Optional[str] = None):
    """Декоратор для логирования функций и вывода результатов в консоль или файл"""

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):  # type: ignore
            try:
                result = func(*args, **kwargs)
                write_result(f"\n{func.__name__} ok\n", filename=filename)
            except Exception as e:
                write_result(
                    f"\n{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n", filename=filename
                )
                raise e

            return result

        return inner

    return decorator
