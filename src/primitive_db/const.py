META_FILE = "db_meta.json"
FILE_ENCODING = "utf-8"
JSON_INDENT = 4

ID_COLUMN = "ID"
TYPE_INT = "int"
TYPE_STR = "str"
TYPE_BOOL = "bool"
ID_TYPE = TYPE_INT
VALID_TYPES = (TYPE_INT, TYPE_STR, TYPE_BOOL)

COLUMN_SEPARATOR = ":"

CMD_EXIT = "exit"
CMD_HELP = "help"
CMD_CREATE_TABLE = "create_table"
CMD_DROP_TABLE = "drop_table"
CMD_LIST_TABLES = "list_tables"

MIN_CREATE_ARGS = 3
SINGLE_TABLE_ARGS = 2

PROMPT_TEXT = ">>>Введите команду: "

HELP_TEXT = """
***Операции с таблицами и данными***

Функции:
<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу
<command> info <имя_таблицы> - информация о таблице
<command> insert into <имя_таблицы> values (<значение1>, ...) - создать запись
<command> select from <имя_таблицы> - прочитать все записи
<command> select from <имя_таблицы> where <столбец> = <значение> - по условию
<command> update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение>
    - обновить запись
<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись

Общие команды:
<command> exit - выход из программы
<command> help - справочная информация
"""

MSG_UNKNOWN_COMMAND = "Функции {command} нет. Попробуйте снова."
MSG_INVALID_VALUE = "Некорректное значение: {value}. Попробуйте снова."
MSG_NO_TABLES = "Таблиц пока нет."

ERR_TABLE_EXISTS = 'Ошибка: Таблица "{name}" уже существует.'
ERR_TABLE_MISSING = 'Ошибка: Таблица "{name}" не существует.'

MSG_TABLE_CREATED = 'Таблица "{name}" успешно создана со столбцами: {columns}'
MSG_TABLE_DROPPED = 'Таблица "{name}" успешно удалена.'


DATA_DIR = "data"

QUOTES = ('"', "'")
BOOL_LITERALS = {"true": True, "false": False}
KEYWORD_SET = " set "
KEYWORD_WHERE = " where "
KEYWORD_VALUES = "values"
KEYWORD_INTO = "into"
KEYWORD_FROM = "from"
EQUALS_SIGN = "="
COMMA = ","

CMD_INFO = "info"
CMD_INSERT = "insert"
CMD_SELECT = "select"
CMD_UPDATE = "update"
CMD_DELETE = "delete"

TYPE_CLASSES = {TYPE_INT: int, TYPE_STR: str, TYPE_BOOL: bool}

MSG_NO_RECORDS = "Записи по заданному условию не найдены."
ERR_COLUMN_MISSING = 'Ошибка: Столбец "{column}" не найден в таблице "{name}".'
ERR_VALUES_COUNT = "Ошибка: Ожидалось значений: {expected}, получено: {actual}."
ERR_ID_IMMUTABLE = "Ошибка: Столбец ID изменять нельзя."

MSG_RECORD_ADDED = 'Запись с ID={ids} успешно добавлена в таблицу "{name}".'
MSG_RECORD_UPDATED = 'Запись с ID={ids} в таблице "{name}" успешно обновлена.'
MSG_RECORD_DELETED = 'Запись с ID={ids} успешно удалена из таблицы "{name}".'
MSG_TABLE_INFO = (
    "Таблица: {name}\nСтолбцы: {columns}\nКоличество записей: {count}"
)