import time

from primitive_db.const import (
    CONFIRM_PROMPT,
    CONFIRM_YES,
    LOG_TIME_TEMPLATE,
    MSG_CANCELLED,
    MSG_FILE_NOT_FOUND,
    MSG_UNEXPECTED,
)


def _copy_metadata(wrapper, func):
    """Переносит имя и docstring исходной функции на обёртку."""
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


def handle_db_errors(func):
    """Перехватывает типичные ошибки и печатает понятное сообщение."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(MSG_FILE_NOT_FOUND)
        except KeyError as error:
            print(error.args[0] if error.args else error)
        except ValueError as error:
            print(error)
        except Exception as error:
            print(MSG_UNEXPECTED.format(error=error))
        return None

    return _copy_metadata(wrapper, func)


def confirm_action(action_name):
    """Фабрика декораторов: просит подтвердить опасную операцию."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                answer = input(CONFIRM_PROMPT.format(action=action_name))
            except EOFError:
                answer = ""
            if answer.strip().lower() != CONFIRM_YES:
                print(MSG_CANCELLED)
                return None
            return func(*args, **kwargs)

        return _copy_metadata(wrapper, func)

    return decorator


def log_time(func):
    """Замеряет и печатает время выполнения функции."""

    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start
        print(LOG_TIME_TEMPLATE.format(name=func.__name__, seconds=elapsed))
        return result

    return _copy_metadata(wrapper, func)


def create_cacher():
    """Создаёт функцию cache_result с кэшем в замыкании."""
    cache = {}

    def cache_result(key, value_func):
        """Возвращает значение из кэша или вычисляет его через value_func."""
        if key not in cache:
            cache[key] = value_func()
        return cache[key]

    return cache_result