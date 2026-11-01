from primitive_db.const import (
    BOOL_LITERALS,
    COMMA,
    EQUALS_SIGN,
    KEYWORD_FROM,
    KEYWORD_INTO,
    KEYWORD_SET,
    KEYWORD_VALUES,
    KEYWORD_WHERE,
    QUOTES,
)


def find_outside_quotes(text, token):
    """Возвращает индекс token (без учёта регистра) вне кавычек или -1."""
    lowered = text.lower()
    quote = None
    for index, char in enumerate(text):
        if quote:
            if char == quote:
                quote = None
        elif char in QUOTES:
            quote = char
        elif lowered.startswith(token, index):
            return index
    return -1


def split_outside_quotes(text, separator):
    """Делит строку по separator, не трогая разделители внутри кавычек."""
    parts = []
    current = []
    quote = None
    for char in text:
        if quote:
            current.append(char)
            if char == quote:
                quote = None
        elif char in QUOTES:
            quote = char
            current.append(char)
        elif char == separator:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
    if quote:
        raise ValueError(text)
    parts.append("".join(current))
    return [part.strip() for part in parts]


def parse_value(raw):
    """Превращает литерал в значение: "text" -> str, 28 -> int, true -> bool."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] in QUOTES and raw[-1] == raw[0]:
        return raw[1:-1]
    lowered = raw.lower()
    if lowered in BOOL_LITERALS:
        return BOOL_LITERALS[lowered]
    try:
        return int(raw)
    except ValueError:
        raise ValueError(raw) from None


def parse_condition(text):
    """Разбирает 'age = 28' в {'age': 28}."""
    parts = split_outside_quotes(text, EQUALS_SIGN)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError(text.strip())
    return {parts[0]: parse_value(parts[1])}


def parse_set(text):
    """Разбирает 'age = 29, name = "Ann"' в словарь новых значений."""
    clause = {}
    for assignment in split_outside_quotes(text, COMMA):
        clause.update(parse_condition(assignment))
    return clause


def parse_values(text):
    """Разбирает '("Ann", 28, true)' в список значений."""
    text = text.strip()
    if not (text.startswith("(") and text.endswith(")")):
        raise ValueError(text)
    return [parse_value(part) for part in split_outside_quotes(text[1:-1], COMMA)]


def _split_table_and_where(rest, command, where_required):
    """Делит '<таблица> [where <условие>]' на имя таблицы и условие."""
    index = find_outside_quotes(rest, KEYWORD_WHERE)
    if index == -1:
        if where_required:
            raise ValueError(command)
        table_name, where_clause = rest.strip(), None
    else:
        table_name = rest[:index].strip()
        where_clause = parse_condition(rest[index + len(KEYWORD_WHERE):])
    if not table_name or " " in table_name:
        raise ValueError(command)
    return table_name, where_clause


def parse_insert(command):
    """Разбирает 'insert into <таблица> values (...)'."""
    parts = command.split(None, 3)
    if len(parts) != 4 or parts[1].lower() != KEYWORD_INTO:
        raise ValueError(command)
    rest = parts[3]
    if rest[: len(KEYWORD_VALUES)].lower() != KEYWORD_VALUES:
        raise ValueError(command)
    return parts[2], parse_values(rest[len(KEYWORD_VALUES):])


def parse_select(command):
    """Разбирает 'select from <таблица> [where ...]'."""
    parts = command.split(None, 2)
    if len(parts) != 3 or parts[1].lower() != KEYWORD_FROM:
        raise ValueError(command)
    return _split_table_and_where(parts[2], command, where_required=False)


def parse_delete(command):
    """Разбирает 'delete from <таблица> where ...'."""
    parts = command.split(None, 2)
    if len(parts) != 3 or parts[1].lower() != KEYWORD_FROM:
        raise ValueError(command)
    return _split_table_and_where(parts[2], command, where_required=True)


def parse_update(command):
    """Разбирает 'update <таблица> set ... where ...'."""
    parts = command.split(None, 1)
    if len(parts) != 2:
        raise ValueError(command)
    rest = parts[1]
    set_index = find_outside_quotes(rest, KEYWORD_SET)
    where_index = find_outside_quotes(rest, KEYWORD_WHERE)
    if set_index == -1 or where_index < set_index:
        raise ValueError(command)
    table_name = rest[:set_index].strip()
    if not table_name or " " in table_name:
        raise ValueError(command)
    set_clause = parse_set(rest[set_index + len(KEYWORD_SET):where_index])
    where_clause = parse_condition(rest[where_index + len(KEYWORD_WHERE):])
    return table_name, set_clause, where_clause