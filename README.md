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