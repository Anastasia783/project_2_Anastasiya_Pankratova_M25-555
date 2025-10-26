from .constants import DEFAULT_PROMPT, EXIT_COMMANDS, HELP_MESSAGE
from .utils import load_metadata, save_metadata
from .core import create_table, drop_table, list_tables, format_columns_display
from .parser import parse_command, parse_column_definitions


def print_help():
    """Print the help message."""
    print(HELP_MESSAGE)


def run():
    """Run the database engine main loop."""
    print("***База данных***")
    print_help()
    
    while True:
        try:
            user_input = input(DEFAULT_PROMPT).strip()
            
            if not user_input:
                continue
                
            # Handle exit commands
            if user_input.lower() in EXIT_COMMANDS:
                print("Выход из программы.")
                break
            
            # Parse command
            try:
                command, args = parse_command(user_input)
            except ValueError as e:
                print(f"Ошибка: {str(e)}")
                continue
            
            # Load current metadata
            metadata = load_metadata()
            
            # Process commands
            if command == "help":
                print_help()
                
            elif command == "create_table":
                if len(args) < 2:
                    print("Ошибка: Недостаточно аргументов. Используйте: create_table <имя_таблицы> <столбец1:тип> ...")
                    continue
                
                table_name = args[0]
                column_args = args[1:]
                
                try:
                    columns = parse_column_definitions(column_args)
                    metadata = create_table(metadata, table_name, columns)
                    save_metadata(metadata)
                    
                    table_columns = metadata[table_name]["columns"]
                    columns_str = format_columns_display(table_columns)
                    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')
                    
                except ValueError as e:
                    print(f"Ошибка: {str(e)}")
                    
            elif command == "list_tables":
                tables = list_tables(metadata)
                if tables:
                    for table in tables:
                        print(f"- {table}")
                else:
                    print("Нет созданных таблиц.")
                    
            elif command == "drop_table":
                if len(args) != 1:
                    print("Ошибка: Неверное количество аргументов. Используйте: drop_table <имя_таблицы>")
                    continue
                
                table_name = args[0]
                
                try:
                    metadata = drop_table(metadata, table_name)
                    save_metadata(metadata)
                    print(f'Таблица "{table_name}" успешно удалена.')
                    
                except ValueError as e:
                    print(f"Ошибка: {str(e)}")
                    
            else:
                print(f"Функции '{command}' нет. Попробуйте снова.")
                
        except KeyboardInterrupt:
            print("\nВыход из программы.")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {str(e)}")