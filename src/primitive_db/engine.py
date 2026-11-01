import shlex

import prompt

from primitive_db import core
from primitive_db.const import (
    CMD_CREATE_TABLE,
    CMD_DROP_TABLE,
    CMD_EXIT,
    CMD_HELP,
    CMD_LIST_TABLES,
    ERR_TABLE_MISSING,
    HELP_TEXT,
    META_FILE,
    MIN_CREATE_ARGS,
    MSG_INVALID_VALUE,
    MSG_NO_TABLES,
    MSG_TABLE_CREATED,
    MSG_TABLE_DROPPED,
    MSG_UNKNOWN_COMMAND,
    PROMPT_TEXT,
    SINGLE_TABLE_ARGS,
)
from primitive_db.utils import format_columns, load_metadata, save_metadata


def print_help():
    """Печатает справку по командам."""
    print(HELP_TEXT)


def _split_args(user_input):
    """Разбирает строку на аргументы через shlex."""
    try:
        return shlex.split(user_input)
    except ValueError:
        raise ValueError(user_input) from None


def _require_table(metadata, table_name):
    """Проверяет существование таблицы, при отсутствии печатает ошибку."""
    if table_name in metadata:
        return True
    print(ERR_TABLE_MISSING.format(name=table_name))
    return False


def _handle_create_table(metadata, user_input):
    """Команда create_table."""
    args = _split_args(user_input)
    if len(args) < MIN_CREATE_ARGS:
        raise ValueError(user_input)
    table_name = args[1]
    updated = core.create_table(metadata, table_name, args[2:])
    if updated is None:
        return
    save_metadata(META_FILE, updated)
    columns = format_columns(updated[table_name])
    print(MSG_TABLE_CREATED.format(name=table_name, columns=columns))


def _handle_drop_table(metadata, user_input):
    """Команда drop_table."""
    args = _split_args(user_input)
    if len(args) != SINGLE_TABLE_ARGS:
        raise ValueError(user_input)
    table_name = args[1]
    if not _require_table(metadata, table_name):
        return
    updated = core.drop_table(metadata, table_name)
    if updated is None:
        return
    save_metadata(META_FILE, updated)
    print(MSG_TABLE_DROPPED.format(name=table_name))


def _handle_list_tables(metadata, user_input):
    """Команда list_tables."""
    if not metadata:
        print(MSG_NO_TABLES)
    for table_name in metadata:
        print(f"- {table_name}")


def process_command(metadata, user_input):
    """Выполняет одну команду; возвращает False, если нужно выйти."""
    handlers = {
        CMD_CREATE_TABLE: _handle_create_table,
        CMD_DROP_TABLE: _handle_drop_table,
        CMD_LIST_TABLES: _handle_list_tables,
    }
    command = user_input.split()[0].lower()
    if command == CMD_EXIT:
        return False
    if command == CMD_HELP:
        print_help()
        return True
    handler = handlers.get(command)
    if handler is None:
        print(MSG_UNKNOWN_COMMAND.format(command=command))
        return True
    try:
        handler(metadata, user_input)
    except ValueError as error:
        print(MSG_INVALID_VALUE.format(value=error))
    return True


def run():
    """Основной цикл программы."""
    print_help()
    while True:
        metadata = load_metadata(META_FILE)
        try:
            user_input = prompt.string(PROMPT_TEXT)
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not process_command(metadata, user_input):
            break