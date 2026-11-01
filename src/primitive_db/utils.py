import json

from primitive_db.const import FILE_ENCODING, JSON_INDENT


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