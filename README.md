# project-2_Vishkyakov_M26-555

# Primitive DB

Консольная «примитивная» база данных на Python. Таблицы и данные хранятся в
JSON-файлах, управление идёт через команды, похожие на SQL. Проект написан в
процедурном стиле (без классов), управляется через uv.

## Установка

    git clone <ссылка-на-репозиторий>
    cd <папка-репозитория>
    make install        # или: uv sync

## Запуск

    make run            # или: uv run database

## Управление таблицами

| Команда | Описание |
|---|---|
| create_table <имя> <столбец:тип> ... | создать таблицу (ID добавляется автоматически) |
| list_tables | показать список таблиц |
| drop_table <имя> | удалить таблицу |
| help / exit | справка / выход |

Типы столбцов: int, str, bool.

Пример:

    >>>Введите команду: create_table users name:str age:int is_active:bool
    Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool
    >>>Введите команду: list_tables
    - users
    >>>Введите команду: drop_table users
    Таблица "users" успешно удалена.


## CRUD-операции

Строковые значения всегда заключаются в кавычки. Значение ID указывать не нужно.

| Команда | Описание |
|---|---|
| insert into <таблица> values (<знач1>, <знач2>, ...) | добавить запись |
| select from <таблица> | все записи |
| select from <таблица> where <столбец> = <значение> | записи по условию |
| update <таблица> set <столбец> = <значение> where <столбец> = <значение> | обновить |
| delete from <таблица> where <столбец> = <значение> | удалить |
| info <таблица> | столбцы и количество записей |

Пример:

    >>>Введите команду: insert into users values ("Matthew", 22, true)
    Запись с ID=1 успешно добавлена в таблицу "users".
    >>>Введите команду: select from users where age = 22
    +----+---------+-----+-----------+
    | ID |  name   | age | is_active |
    +----+---------+-----+-----------+
    | 1  | Matthew |  22 |    True   |
    +----+---------+-----+-----------+


## Обработка ошибок, подтверждение, кэш

- `handle_db_errors` перехватывает `KeyError`, `ValueError`, `FileNotFoundError`
  и печатает понятное сообщение вместо traceback;
- `confirm_action` спрашивает `[y/n]` перед `drop_table` и `delete`;
- `log_time` печатает время выполнения `insert` и `select`;
- `create_cacher` создаёт замыкание-кэш, он используется в `select`.

Пример подтверждения:

    >>>Введите команду: delete from users where ID = 1
    Вы уверены, что хотите выполнить "удаление записи"? [y/n]: y
    Запись с ID=1 успешно удалена из таблицы "users".


## Структура проекта

    src/primitive_db/
    ├── main.py        # точка входа
    ├── engine.py      # главный цикл и обработка команд
    ├── core.py        # логика таблиц и CRUD
    ├── parser.py      # разбор values / set / where
    ├── utils.py       # работа с JSON-файлами
    ├── decorators.py  # декораторы и кэш-замыкание
    └── const.py       # константы и тексты сообщений

Данные хранятся в `db_meta.json` (схемы таблиц) и `data/<таблица>.json`.

## Проверка кода

    make lint           # ruff check .

## Установка как консольной команды

    make build
    make package-install   # uv tool install dist/*.whl
    database

## Демонстрация
