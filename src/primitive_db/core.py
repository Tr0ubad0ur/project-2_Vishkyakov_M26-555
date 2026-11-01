from primitive_db.const import (
    COLUMN_SEPARATOR,
    ERR_TABLE_EXISTS,
    ERR_TABLE_MISSING,
    ID_COLUMN,
    ID_TYPE,
    MSG_INVALID_VALUE,
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