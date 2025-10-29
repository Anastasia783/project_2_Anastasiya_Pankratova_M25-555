META_FILE = "db_meta.json"
DATA_DIR = "data"
VALID_TYPES = {"int", "str", "bool"}
DEFAULT_PROMPT = ">>> Введите команду: "
COMMAND_HISTORY_FILE = ".command_history"

HELP_MESSAGE = """
***Операции с данными***

Функции:
<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись
<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию
<command> select from <имя_таблицы> - прочитать все записи
<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись
<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись
<command> info <имя_таблицы> - вывести информацию о таблице
<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу
<command> exit - выход из программы
<command> help - справочная информация
"""
