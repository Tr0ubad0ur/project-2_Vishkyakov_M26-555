import json

from primitive_db.const import (
    ACTION_DELETE_RECORD,
    ACTION_DROP_TABLE,
    COLUMN_SEPARATOR,
    ERR_COLUMN_MISSING,
    ERR_ID_IMMUTABLE,
    ERR_TABLE_EXISTS,
    ERR_TABLE_MISSING,
    ERR_VALUES_COUNT,
    ID_COLUMN,
    ID_TYPE,
    MSG_INVALID_VALUE,
    TYPE_CLASSES,
    VALID_TYPES,
)
from primitive_db.decorators import (
    confirm_action,
    create_cacher,
    handle_db_errors,
    log_time,
)

_select_cache = create_cacher()


def _get_columns(metadata, table_name):
    """Возвращает схему таблицы или бросает KeyError, если таблицы нет."""
    if table_name not in metadata:
        raise KeyError(ERR_TABLE_MISSING.format(name=table_name))
    return metadata[table_name]


def _validate_value(value, column_type):
    """Проверяет, что значение соответствует типу столбца."""
    if type(value) is not TYPE_CLASSES[column_type]:
        raise ValueError(MSG_INVALID_VALUE.format(value=value))


def _matches(record, where_clause):
    """Проверяет, подходит ли запись под условие."""
    return all(record.get(col) == val for col, val in where_clause.items())


def _next_id(table_data):
    """Генерирует следующий ID: максимальный + 1."""
    return max((record[ID_COLUMN] for record in table_data), default=0) + 1


def matching_ids(table_data, where_clause):
    """Возвращает ID записей, подходящих под условие."""
    return [r[ID_COLUMN] for r in table_data if _matches(r, where_clause)]


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создаёт таблицу; столбец ID:int добавляется автоматически."""
    if table_name in metadata:
        raise ValueError(ERR_TABLE_EXISTS.format(name=table_name))
    if not table_name.isidentifier():
        raise ValueError(MSG_INVALID_VALUE.format(value=table_name))
    table_columns = {ID_COLUMN: ID_TYPE}
    for column in columns:
        name, separator, column_type = column.partition(COLUMN_SEPARATOR)
        is_valid = (
            bool(separator)
            and name.isidentifier()
            and column_type in VALID_TYPES
            and name.lower() != ID_COLUMN.lower()
            and name not in table_columns
        )
        if not is_valid:
            raise ValueError(MSG_INVALID_VALUE.format(value=column))
        table_columns[name] = column_type
    metadata[table_name] = table_columns
    return metadata


@handle_db_errors
@confirm_action(ACTION_DROP_TABLE)
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    _get_columns(metadata, table_name)
    del metadata[table_name]
    return metadata


@handle_db_errors
def validate_clause(metadata, table_name, clause):
    """Проверяет столбцы и типы значений в where/set; True, если всё верно."""
    columns = _get_columns(metadata, table_name)
    for column, value in clause.items():
        if column not in columns:
            raise KeyError(ERR_COLUMN_MISSING.format(column=column, name=table_name))
        _validate_value(value, columns[column])
    return True


@handle_db_errors
@log_time
def insert(metadata, table_name, table_data, values):
    """Добавляет запись с автоматически сгенерированным ID."""
    columns = _get_columns(metadata, table_name)
    user_columns = {n: t for n, t in columns.items() if n != ID_COLUMN}
    if len(values) != len(user_columns):
        raise ValueError(
            ERR_VALUES_COUNT.format(expected=len(user_columns), actual=len(values))
        )
    record = {ID_COLUMN: _next_id(table_data)}
    for (name, column_type), value in zip(user_columns.items(), values):
        _validate_value(value, column_type)
        record[name] = value
    table_data.append(record)
    return table_data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Возвращает все записи или только подходящие под условие (с кэшем)."""
    key = json.dumps([table_data, where_clause], sort_keys=True, ensure_ascii=False)

    def load_rows():
        if not where_clause:
            return list(table_data)
        return [r for r in table_data if _matches(r, where_clause)]

    return _select_cache(key, load_rows)


@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Обновляет поля у записей, подходящих под условие."""
    if ID_COLUMN in set_clause:
        raise ValueError(ERR_ID_IMMUTABLE)
    for record in table_data:
        if _matches(record, where_clause):
            record.update(set_clause)
    return table_data


@handle_db_errors
@confirm_action(ACTION_DELETE_RECORD)
def delete(table_data, where_clause):
    """Удаляет записи, подходящие под условие."""
    return [r for r in table_data if not _matches(r, where_clause)]