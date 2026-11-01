import json
import os

from primitive_db.const import DATA_DIR, FILE_ENCODING, JSON_INDENT


def load_json(filepath, default):
    """Читает JSON-файл; если файла нет, возвращает значение default."""
    try:
        with open(filepath, encoding=FILE_ENCODING) as file:
            return json.load(file)
    except FileNotFoundError:
        return default


def save_json(filepath, data):
    """Сохраняет данные в JSON-файл."""
    with open(filepath, "w", encoding=FILE_ENCODING) as file:
        json.dump(data, file, indent=JSON_INDENT, ensure_ascii=False)


def load_metadata(filepath):
    """Загружает метаданные таблиц; если файла нет, возвращает {}."""
    return load_json(filepath, {})


def save_metadata(filepath, data):
    """Сохраняет метаданные таблиц в JSON-файл."""
    save_json(filepath, data)


def format_columns(columns):
    """Форматирует столбцы в строку вида 'ID:int, name:str'."""
    return ", ".join(f"{name}:{kind}" for name, kind in columns.items())



def get_table_path(table_name):
    """Возвращает путь к файлу с данными таблицы."""
    return os.path.join(DATA_DIR, f"{table_name}.json")


def load_table_data(table_name):
    """Загружает записи таблицы; если файла нет, возвращает []."""
    return load_json(get_table_path(table_name), [])


def save_table_data(table_name, data):
    """Сохраняет записи таблицы в data/<имя_таблицы>.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    save_json(get_table_path(table_name), data)


def delete_table_data(table_name):
    """Удаляет файл с данными таблицы, если он существует."""
    path = get_table_path(table_name)
    if os.path.exists(path):
        os.remove(path)