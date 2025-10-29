import shlex
from typing import List, Tuple

from .constants import DEFAULT_PROMPT
from .core import (
    create_table,
    delete_from,
    drop_table,
    info_table,
    insert_into,
    select_from,
    update_table,
)
from .decorators import handle_db_errors
from .parser import (
    parse_create_table,
    parse_set_clause,
    parse_values_clause,
    parse_where_condition,
)


def parse_command(command: str) -> Tuple[str, List[str]]:
    """Парсит команду и возвращает основную команду и части."""
    try:
        parts = shlex.split(command.strip())
        if not parts:
            return "", []

        main_command = parts[0].upper()
        return main_command, parts
    except Exception:
        return "ERROR", []


@handle_db_errors
def execute_command(command: str) -> str:
    """Выполняет команду базы данных."""
    main_command, parts = parse_command(command)

    if not main_command:
        return ""

    command_handlers = {
        "CREATE": handle_create_table,
        "DROP": handle_drop_table,
        "INSERT": handle_insert,
        "SELECT": handle_select,
        "UPDATE": handle_update,
        "DELETE": handle_delete,
        "INFO": handle_info,
        "EXIT": lambda _: "EXIT",
        "HELP": lambda _: get_help(),
    }

    handler = command_handlers.get(main_command)
    if handler:
        return handler(parts)
    else:
        return f"Error: Unknown command '{main_command}'"


def handle_create_table(parts: List[str]) -> str:
    """Обрабатывает команду CREATE TABLE."""
    if len(parts) < 4:
        return "Error: Invalid CREATE TABLE syntax. Use: CREATE TABLE table_name (column1 type1, ...)"

    try:
        table_name, columns = parse_create_table(parts)
        return create_table(table_name, columns)
    except Exception as e:
        return f"Error: {str(e)}"


def handle_drop_table(parts: List[str]) -> str:
    """Обрабатывает команду DROP TABLE."""
    if len(parts) < 3 or parts[1].upper() != 'TABLE':
        return "Error: Invalid DROP TABLE syntax. Use: DROP TABLE table_name"

    table_name = parts[2]
    return drop_table(table_name)


def handle_insert(parts: List[str]) -> str:
    """Обрабатывает команду INSERT INTO."""
    if len(parts) < 4 or parts[1].upper() != 'INTO':
        return "Error: Invalid INSERT syntax. Use: INSERT INTO table_name VALUES (...)"

    table_name = parts[2]

    # Находим часть VALUES
    command_str = ' '.join(parts)
    values_index = command_str.upper().find('VALUES')
    if values_index == -1:
        return "Error: VALUES clause not found"

    values_str = command_str[values_index + 6:].strip()
    try:
        values = parse_values_clause(values_str)
        return insert_into(table_name, values)
    except Exception as e:
        return f"Error: {str(e)}"


def handle_select(parts: List[str]) -> str:
    """Обрабатывает команду SELECT FROM."""
    if len(parts) < 3 or parts[1].upper() != 'FROM':
        return "Error: Invalid SELECT syntax. Use: SELECT FROM table_name [WHERE condition]"

    table_name = parts[2]

    # Обрабатываем WHERE условие если есть
    where_condition = {}
    command_str = ' '.join(parts)
    where_index = command_str.upper().find('WHERE')
    if where_index != -1:
        where_clause = command_str[where_index + 5:].strip()
        where_condition = parse_where_condition(where_clause)

    return select_from(table_name, where_condition)


def handle_update(parts: List[str]) -> str:
    """Обрабатывает команду UPDATE."""
    if len(parts) < 4 or parts[2].upper() != 'SET':
        return "Error: Invalid UPDATE syntax. Use: UPDATE table_name SET column=value [WHERE condition]"

    table_name = parts[1]

    # Находим SET и WHERE части
    command_str = ' '.join(parts)
    set_index = command_str.upper().find('SET')
    where_index = command_str.upper().find('WHERE')

    set_clause = command_str[set_index + 3:where_index].strip() if where_index != -1 else command_str[set_index + 3:].strip()

    try:
        updates = parse_set_clause(set_clause)
    except Exception as e:
        return f"Error parsing SET clause: {str(e)}"

    # Обрабатываем WHERE условие если есть
    where_condition = {}
    if where_index != -1:
        where_clause = command_str[where_index + 5:].strip()
        where_condition = parse_where_condition(where_clause)

    return update_table(table_name, updates, where_condition)


def handle_delete(parts: List[str]) -> str:
    """Обрабатывает команду DELETE FROM."""
    if len(parts) < 3 or parts[1].upper() != 'FROM':
        return "Error: Invalid DELETE syntax. Use: DELETE FROM table_name [WHERE condition]"

    table_name = parts[2]

    # Обрабатываем WHERE условие если есть
    where_condition = {}
    command_str = ' '.join(parts)
    where_index = command_str.upper().find('WHERE')
    if where_index != -1:
        where_clause = command_str[where_index + 5:].strip()
        where_condition = parse_where_condition(where_clause)

    return delete_from(table_name, where_condition)


def handle_info(parts: List[str]) -> str:
    """Обрабатывает команду INFO."""
    if len(parts) < 2:
        return "Error: Invalid INFO syntax. Use: INFO table_name"

    table_name = parts[1]
    return info_table(table_name)


def get_help() -> str:
    """Возвращает справку по командам."""
    help_text = """
Доступные команды:

CREATE TABLE имя_таблицы (столбе1 тип1, столбе2 тип2, ...)
    - Создает новую таблицу с указанными столбцами
    - Поддерживаемые типы: int, str, bool

DROP TABLE имя_таблицы
    - Удаляет таблицу и все ее данные

INSERT INTO имя_таблицы VALUES (значение1, значение2, ...)
    - Вставляет новую запись в таблицу (ID генерируется автоматически)

SELECT FROM имя_таблицы [WHERE условие]
    - Выбирает данные из таблицы

UPDATE имя_таблицы SET столбец1=новое_значение1 [WHERE условие]
    - Обновляет данные в таблице

DELETE FROM имя_таблицы [WHERE условие]
    - Удаляет данные из таблицы

INFO имя_таблицы
    - Показывает информацию о таблице

HELP
    - Показывает эту справку

EXIT
    - Выход из программы

Примеры:
  CREATE TABLE users (name str, age int, is_active bool)
  INSERT INTO users VALUES ("Sergei", 28, true)
  SELECT FROM users WHERE age = 28
  UPDATE users SET age = 29 WHERE name = "Sergei"
  DELETE FROM users WHERE ID = 1
  INFO users
"""
    return help_text.strip()


def display_welcome_message() -> None:
    """Выводит приветственное сообщение."""
    print("***Операции с данными***")
    print()
    print("Функции:")
    print("insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.")
    print("select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")
    print("select from <имя_таблицы> - прочитать все записи.")
    print("update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.")
    print("delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")
    print("info <имя_таблицы> - вывести информацию о таблице.")
    print("exit - выход из программы")
    print("help - справочная информация")
    print()


def run_database() -> None:
    """Основной цикл базы данных."""
    display_welcome_message()

    while True:
        try:
            user_input = input(DEFAULT_PROMPT).strip()

            if not user_input:
                continue

            result = execute_command(user_input)

            if result == "EXIT":
                print("Goodbye!")
                break
            elif result:
                print(result)

        except KeyboardInterrupt:
            print("\nUse 'EXIT' to quit")
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    run_database()
