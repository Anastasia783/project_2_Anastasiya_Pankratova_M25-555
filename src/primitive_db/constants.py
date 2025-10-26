META_FILE = "db_meta.json"
DATA_DIR = "data"
VALID_TYPES = {"int", "str", "bool"}
DEFAULT_PROMPT = ">>>Введите команду: "
EXIT_COMMANDS = {"exit", "quit", "q"}

HELP_MESSAGE = """
***Процесс работы с таблицей***
Функции:
<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу
<command> exit - выход из программы
<command> help - справочная информация
"""