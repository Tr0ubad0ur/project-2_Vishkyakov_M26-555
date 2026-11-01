"""Главный цикл программы: ввод команд и вызов логики из core."""

import shlex

import prompt
from prettytable import PrettyTable

from primitive_db import core, parser
from primitive_db.const import (
    CMD_CREATE_TABLE,
    CMD_DELETE,
    CMD_DROP_TABLE,
    CMD_EXIT,
    CMD_HELP,
    CMD_INFO,
    CMD_INSERT,
    CMD_LIST_TABLES,
    CMD_SELECT,
    CMD_UPDATE,
    ERR_TABLE_MISSING,
    HELP_TEXT,
    ID_COLUMN,
    META_FILE,
    MIN_CREATE_ARGS,
    MSG_INVALID_VALUE,
    MSG_NO_RECORDS,
    MSG_NO_TABLES,
    MSG_RECORD_ADDED,
    MSG_RECORD_DELETED,
    MSG_RECORD_UPDATED,
    MSG_TABLE_CREATED,
    MSG_TABLE_DROPPED,
    MSG_TABLE_INFO,
    MSG_UNKNOWN_COMMAND,
    PROMPT_TEXT,
    SINGLE_TABLE_ARGS,
)
from primitive_db.utils import (
    delete_table_data,
    format_columns,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


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


def _ids_text(ids):
    """Форматирует список ID для вывода."""
    return ", ".join(str(record_id) for record_id in ids)


def _print_records(columns, rows):
    """Печатает записи в виде таблицы PrettyTable."""
    names = list(columns)
    pretty = PrettyTable(names)
    for row in rows:
        pretty.add_row([row.get(name) for name in names])
    print(pretty)


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
    delete_table_data(table_name)
    print(MSG_TABLE_DROPPED.format(name=table_name))


def _handle_list_tables(metadata, user_input):
    """Команда list_tables."""
    if not metadata:
        print(MSG_NO_TABLES)
    for table_name in metadata:
        print(f"- {table_name}")


def _handle_info(metadata, user_input):
    """Команда info."""
    args = _split_args(user_input)
    if len(args) != SINGLE_TABLE_ARGS:
        raise ValueError(user_input)
    table_name = args[1]
    if not _require_table(metadata, table_name):
        return
    print(
        MSG_TABLE_INFO.format(
            name=table_name,
            columns=format_columns(metadata[table_name]),
            count=len(load_table_data(table_name)),
        )
    )


def _handle_insert(metadata, user_input):
    """Команда insert into ... values (...)."""
    table_name, values = parser.parse_insert(user_input)
    if not _require_table(metadata, table_name):
        return
    table_data = load_table_data(table_name)
    updated = core.insert(metadata, table_name, table_data, values)
    if updated is None:
        return
    save_table_data(table_name, updated)
    print(MSG_RECORD_ADDED.format(ids=updated[-1][ID_COLUMN], name=table_name))


def _handle_select(metadata, user_input):
    """Команда select from ... [where ...]."""
    table_name, where_clause = parser.parse_select(user_input)
    if not _require_table(metadata, table_name):
        return
    if where_clause and not core.validate_clause(metadata, table_name, where_clause):
        return
    rows = core.select(load_table_data(table_name), where_clause)
    if rows is not None:
        _print_records(metadata[table_name], rows)


def _handle_update(metadata, user_input):
    """Команда update ... set ... where ..."""
    table_name, set_clause, where_clause = parser.parse_update(user_input)
    if not _require_table(metadata, table_name):
        return
    for clause in (set_clause, where_clause):
        if not core.validate_clause(metadata, table_name, clause):
            return
    table_data = load_table_data(table_name)
    ids = core.matching_ids(table_data, where_clause)
    if not ids:
        print(MSG_NO_RECORDS)
        return
    updated = core.update(table_data, set_clause, where_clause)
    if updated is None:
        return
    save_table_data(table_name, updated)
    print(MSG_RECORD_UPDATED.format(ids=_ids_text(ids), name=table_name))


def _handle_delete(metadata, user_input):
    """Команда delete from ... where ..."""
    table_name, where_clause = parser.parse_delete(user_input)
    if not _require_table(metadata, table_name):
        return
    if not core.validate_clause(metadata, table_name, where_clause):
        return
    table_data = load_table_data(table_name)
    ids = core.matching_ids(table_data, where_clause)
    if not ids:
        print(MSG_NO_RECORDS)
        return
    updated = core.delete(table_data, where_clause)
    if updated is None:
        return
    save_table_data(table_name, updated)
    print(MSG_RECORD_DELETED.format(ids=_ids_text(ids), name=table_name))


def process_command(metadata, user_input):
    """Выполняет одну команду; возвращает False, если нужно выйти."""
    handlers = {
        CMD_CREATE_TABLE: _handle_create_table,
        CMD_DROP_TABLE: _handle_drop_table,
        CMD_LIST_TABLES: _handle_list_tables,
        CMD_INFO: _handle_info,
        CMD_INSERT: _handle_insert,
        CMD_SELECT: _handle_select,
        CMD_UPDATE: _handle_update,
        CMD_DELETE: _handle_delete,
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