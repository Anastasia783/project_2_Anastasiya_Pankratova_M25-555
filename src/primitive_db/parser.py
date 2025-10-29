from typing import Any, Dict, List, Tuple


def parse_where_condition(where_clause: str) -> Dict[str, Any]:
    """Парсит условие WHERE в словарь."""
    if not where_clause:
        return {}

    operators = ['=', '!=', '>', '<', '>=', '<=']

    for op in operators:
        if op in where_clause:
            parts = where_clause.split(op, 1)
            if len(parts) == 2:
                column = parts[0].strip()
                value = parse_value(parts[1].strip())
                return {'column': column, 'operator': op, 'value': value}

    return {}


def parse_set_clause(set_clause: str) -> Dict[str, Any]:
    """Парсит предложение SET для UPDATE."""
    updates = {}
    if not set_clause:
        return updates

    assignments = [a.strip() for a in set_clause.split(',')]

    for assignment in assignments:
        if '=' in assignment:
            col, val = assignment.split('=', 1)
            col = col.strip()
            val = parse_value(val.strip())
            updates[col] = val

    return updates


def parse_values_clause(values_clause: str) -> List[Any]:
    """Парсит предложение VALUES для INSERT."""
    if not values_clause:
        return []

    # Удаляем внешние скобки если есть
    values_clause = values_clause.strip()
    if values_clause.startswith('(') and values_clause.endswith(')'):
        values_clause = values_clause[1:-1].strip()

    # Ручной парсинг значений с учетом кавычек
    values = []
    current_value = ""
    in_quotes = False
    quote_char = None
    paren_depth = 0

    i = 0
    while i < len(values_clause):
        char = values_clause[i]

        if char in ['"', "'"] and not in_quotes:
            in_quotes = True
            quote_char = char
            current_value += char
        elif char == quote_char and in_quotes:
            in_quotes = False
            current_value += char
        elif char == '(' and not in_quotes:
            paren_depth += 1
            current_value += char
        elif char == ')' and not in_quotes:
            paren_depth -= 1
            current_value += char
        elif char == ',' and not in_quotes and paren_depth == 0:
            # Нашли разделитель между значениями
            if current_value.strip():
                values.append(parse_value(current_value.strip()))
            current_value = ""
        else:
            current_value += char

        i += 1

    # Добавляем последнее значение
    if current_value.strip():
        values.append(parse_value(current_value.strip()))

    return values


def parse_value(value_str: str) -> Any:
    """Парсит значение в соответствующий тип."""
    if not value_str:
        return ""

    value_str = value_str.strip()

    # Boolean - обрабатываем первым
    if value_str.lower() in ['true', 'false']:
        return value_str.lower() == 'true'

    # Если строка в кавычках - возвращаем как строку без кавычек
    if len(value_str) >= 2 and value_str[0] in ['"', "'"] and value_str[-1] in ['"', "'"]:
        return value_str[1:-1]

    # Пробуем integer
    try:
        # Убираем возможные запятые в конце
        if value_str.endswith(','):
            value_str = value_str[:-1]
        return int(value_str)
    except ValueError:
        pass

    # Если это число с плавающей точкой
    try:
        if value_str.endswith(','):
            value_str = value_str[:-1]
        return float(value_str)
    except ValueError:
        pass

    # Возвращаем как строку
    return value_str


def parse_create_table(command_parts: List[str]) -> Tuple[str, Dict[str, str]]:
    """Парсит команду CREATE TABLE."""
    if len(command_parts) < 4:
        raise ValueError("Invalid CREATE TABLE syntax")

    table_name = command_parts[2]

    # Объединяем оставшиеся части для получения определения столбцов
    columns_str = ' '.join(command_parts[3:])

    if not columns_str.startswith('(') or not columns_str.endswith(')'):
        raise ValueError("Column definitions must be in parentheses")

    columns_str = columns_str[1:-1].strip()
    columns = {}

    for col_def in columns_str.split(','):
        col_def = col_def.strip()
        if not col_def:
            continue

        parts = col_def.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid column definition: {col_def}")

        col_name = parts[0]
        col_type = parts[1].lower()
        columns[col_name] = col_type

    return table_name, columns
