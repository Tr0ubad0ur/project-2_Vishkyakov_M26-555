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
***Процесс работы с таблицей***

Функции:
<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу

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