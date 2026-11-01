from primitive_db.const import (
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


def create_table(metadata, table_name, columns):
    """Создаёт таблицу; столбец ID:int добавляется автоматически."""
    if table_name in metadata:
        print(ERR_TABLE_EXISTS.format(name=table_name))
        return None
    if not table_name.isidentifier():
        print(MSG_INVALID_VALUE.format(value=table_name))
        return None
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
            print(MSG_INVALID_VALUE.format(value=column))
            return None
        table_columns[name] = column_type
    metadata[table_name] = table_columns
    return metadata


def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(ERR_TABLE_MISSING.format(name=table_name))
        return None
    del metadata[table_name]
    return metadata



def _is_valid_value(value, column_type):
    """Проверяет, что значение соответствует типу столбца."""
    return type(value) is TYPE_CLASSES[column_type]


def _matches(record, where_clause):
    """Проверяет, подходит ли запись под условие."""
    return all(record.get(col) == val for col, val in where_clause.items())


def _next_id(table_data):
    """Генерирует следующий ID: максимальный + 1."""
    return max((record[ID_COLUMN] for record in table_data), default=0) + 1


def matching_ids(table_data, where_clause):
    """Возвращает ID записей, подходящих под условие."""
    return [r[ID_COLUMN] for r in table_data if _matches(r, where_clause)]


def validate_clause(metadata, table_name, clause):
    """Проверяет столбцы и типы значений в where/set; True, если всё верно."""
    columns = metadata[table_name]
    for column, value in clause.items():
        if column not in columns:
            print(ERR_COLUMN_MISSING.format(column=column, name=table_name))
            return None
        if not _is_valid_value(value, columns[column]):
            print(MSG_INVALID_VALUE.format(value=value))
            return None
    return True


def insert(metadata, table_name, table_data, values):
    """Добавляет запись с автоматически сгенерированным ID."""
    columns = metadata[table_name]
    user_columns = {n: t for n, t in columns.items() if n != ID_COLUMN}
    if len(values) != len(user_columns):
        print(ERR_VALUES_COUNT.format(expected=len(user_columns), actual=len(values)))
        return None
    record = {ID_COLUMN: _next_id(table_data)}
    for (name, column_type), value in zip(user_columns.items(), values):
        if not _is_valid_value(value, column_type):
            print(MSG_INVALID_VALUE.format(value=value))
            return None
        record[name] = value
    table_data.append(record)
    return table_data


def select(table_data, where_clause=None):
    """Возвращает все записи или только подходящие под условие."""
    if not where_clause:
        return list(table_data)
    return [r for r in table_data if _matches(r, where_clause)]


def update(table_data, set_clause, where_clause):
    """Обновляет поля у записей, подходящих под условие."""
    if ID_COLUMN in set_clause:
        print(ERR_ID_IMMUTABLE)
        return None
    for record in table_data:
        if _matches(record, where_clause):
            record.update(set_clause)
    return table_data


def delete(table_data, where_clause):
    """Удаляет записи, подходящие под условие."""
    return [r for r in table_data if not _matches(r, where_clause)]