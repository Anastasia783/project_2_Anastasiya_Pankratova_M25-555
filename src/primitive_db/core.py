from typing import Any, Dict, List

from prettytable import PrettyTable

from .constants import VALID_TYPES
from .decorators import confirm_action, handle_db_errors, log_time
from .utils import (
    get_next_id,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
    table_exists,
)


@handle_db_errors
def create_table(table_name: str, columns: Dict[str, str]) -> str:
    """Создает новую таблицу."""
    metadata = load_metadata()

    if table_name in metadata["tables"]:
        return f"Error: Table '{table_name}' already exists."

    for col_name, col_type in columns.items():
        if col_type not in VALID_TYPES:
            return f"Error: Invalid data type '{col_type}' for column '{col_name}'."

    columns_with_id = {"ID": "int"}
    columns_with_id.update(columns)

    metadata["tables"][table_name] = {"columns": columns_with_id}
    save_metadata(metadata)
    save_table_data(table_name, [])

    return f"Table '{table_name}' created successfully."


@handle_db_errors
@confirm_action("table deletion")
def drop_table(table_name: str) -> str:
    """Удаляет таблицу."""
    metadata = load_metadata()

    if table_name not in metadata["tables"]:
        return f"Error: Table '{table_name}' does not exist."

    del metadata["tables"][table_name]
    save_metadata(metadata)

    import os

    from .utils import get_table_file_path

    try:
        os.remove(get_table_file_path(table_name))
    except FileNotFoundError:
        pass

    return f"Table '{table_name}' dropped successfully."


@handle_db_errors
@log_time
def insert_into(table_name: str, values: List[Any]) -> str:
    """Вставляет данные в таблицу."""
    if not table_exists(table_name):
        return f"Error: Table '{table_name}' does not exist."

    metadata = load_metadata()
    table_meta = metadata["tables"][table_name]
    columns = list(table_meta["columns"].keys())

    expected_values_count = len(columns) - 1
    if len(values) != expected_values_count:
        return f"Error: Expected {expected_values_count} values, got {len(values)}."

    data = load_table_data(table_name)
    new_row = {"ID": get_next_id(data)}

    data_columns = columns[1:]

    for i, col in enumerate(data_columns):
        col_type = table_meta["columns"][col]
        value = values[i]

        try:
            validated_value = validate_and_convert_value(value, col_type, col)
            new_row[col] = validated_value
        except ValueError as e:
            return str(e)

    data.append(new_row)
    save_table_data(table_name, data)

    return f"Запись с ID={new_row['ID']} успешно добавлена в таблицу \"{table_name}\"."


@handle_db_errors
@log_time
def select_from(
    table_name: str,
    where_condition: Dict[str, Any] = None,
) -> str:
    """Выбирает данные из таблицы."""
    if not table_exists(table_name):
        return f"Error: Table '{table_name}' does not exist."

    data = load_table_data(table_name)

    if where_condition:
        filtered_data = []
        for row in data:
            if evaluate_where_condition(row, where_condition):
                filtered_data.append(row)
        data = filtered_data

    if not data:
        return "No records found."

    table = PrettyTable()
    metadata = load_metadata()
    columns = list(metadata["tables"][table_name]["columns"].keys())
    table.field_names = columns

    for row in data:
        table.add_row([row.get(col, "") for col in columns])

    return table.get_string()


def evaluate_where_condition(row: Dict[str, Any], condition: Dict[str, Any]) -> bool:
    """Вычисляет условие WHERE для строки."""
    if not condition:
        return True

    col = condition.get("column")
    op = condition.get("operator")
    value = condition.get("value")

    if col not in row:
        return False

    row_value = row[col]

    try:
        if op == "=":
            return row_value == value
        elif op == "!=":
            return row_value != value
        elif op == ">":
            return row_value > value
        elif op == "<":
            return row_value < value
        elif op == ">=":
            return row_value >= value
        elif op == "<=":
            return row_value <= value
    except TypeError:
        return False

    return False


@handle_db_errors
def update_table(
    table_name: str,
    updates: Dict[str, Any],
    where_condition: Dict[str, Any] = None,
) -> str:
    """Обновляет данные в таблице."""
    if not table_exists(table_name):
        return f"Error: Table '{table_name}' does not exist."

    metadata = load_metadata()
    table_meta = metadata["tables"][table_name]
    data = load_table_data(table_name)
    updated_count = 0
    updated_ids = []

    for row in data:
        if evaluate_where_condition(row, where_condition):
            for col, value in updates.items():
                col_type = table_meta["columns"][col]
                try:
                    validated_value = validate_and_convert_value(value, col_type, col)
                    row[col] = validated_value
                except ValueError as e:
                    return str(e)
            updated_count += 1
            updated_ids.append(row["ID"])

    if updated_count > 0:
        save_table_data(table_name, data)
        if len(updated_ids) == 1:
            return f"Запись с ID={updated_ids[0]} в таблице \"{table_name}\" успешно обновлена."
        else:
            return f"{updated_count} записей в таблице \"{table_name}\" успешно обновлено."

    return "No records matched the condition."


@handle_db_errors
@confirm_action("record deletion")
def delete_from(table_name: str, where_condition: Dict[str, Any] = None) -> str:
    """Удаляет данные из таблицы."""
    if not table_exists(table_name):
        return f"Error: Table '{table_name}' does not exist."

    data = load_table_data(table_name)

    deleted_ids = []
    if where_condition:
        new_data = []
        for row in data:
            if evaluate_where_condition(row, where_condition):
                deleted_ids.append(row["ID"])
            else:
                new_data.append(row)
        data = new_data
    else:
        deleted_ids = [row["ID"] for row in data]
        data = []

    deleted_count = len(deleted_ids)

    if deleted_count > 0:
        save_table_data(table_name, data)
        if deleted_count == 1:
            return f"Запись с ID={deleted_ids[0]} успешно удалена из таблицы \"{table_name}\"."
        else:
            return f"{deleted_count} записей успешно удалено из таблицы \"{table_name}\"."

    return "No records matched the condition."


@handle_db_errors
def info_table(table_name: str) -> str:
    """Выводит информацию о таблице."""
    if not table_exists(table_name):
        return f"Error: Table '{table_name}' does not exist."

    metadata = load_metadata()
    table_meta = metadata["tables"][table_name]
    data = load_table_data(table_name)

    columns_info = ", ".join([
        f"{col}:{typ}" for col, typ in table_meta["columns"].items()
    ])

    result = [
        f"Таблица: {table_name}",
        f"Столбцы: {columns_info}",
        f"Количество записей: {len(data)}"
    ]

    return "\n".join(result)


def validate_and_convert_value(value: Any, expected_type: str, column_name: str) -> Any:
    """Проверяет и преобразует значение к ожидаемому типу."""
    if expected_type == "int" and isinstance(value, int):
        return value
    elif expected_type == "str" and isinstance(value, str):
        return value
    elif expected_type == "bool" and isinstance(value, bool):
        return value

    try:
        if expected_type == "int":
            if isinstance(value, str):
                return int(value)
            elif isinstance(value, bool):
                return int(value)
            else:
                raise ValueError(f"Expected integer for column '{column_name}', got {type(value).__name__}.")

        elif expected_type == "bool":
            if isinstance(value, str):
                if value.lower() in ['true', 'false']:
                    return value.lower() == 'true'
                elif value.isdigit():
                    return bool(int(value))
                else:
                    raise ValueError(f"Expected boolean for column '{column_name}', got string '{value}'.")
            elif isinstance(value, int):
                return bool(value)
            else:
                raise ValueError(f"Expected boolean for column '{column_name}', got {type(value).__name__}.")

        elif expected_type == "str":
            return str(value)

    except (ValueError, TypeError) as e:
        raise ValueError(f"Error converting value '{value}' to {expected_type} for column '{column_name}': {str(e)}") from e

    return value


@handle_db_errors
def show_tables() -> str:
    """Показывает список всех таблиц в базе данных."""
    metadata = load_metadata()

    if not metadata["tables"]:
        return "No tables in database."

    table = PrettyTable()
    table.field_names = ["Table Name", "Columns Count", "Records Count"]

    for table_name, table_meta in metadata["tables"].items():
        data = load_table_data(table_name)
        columns_count = len(table_meta["columns"])
        records_count = len(data)
        table.add_row([table_name, columns_count, records_count])

    return table.get_string()
