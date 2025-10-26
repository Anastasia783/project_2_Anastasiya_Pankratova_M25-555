import shlex
from typing import List, Tuple


def parse_command(user_input: str) -> Tuple[str, List[str]]:
    """Parse user input into command and arguments."""
    try:
        parts = shlex.split(user_input)
        if not parts:
            return "", []
        command = parts[0]
        args = parts[1:]
        return command, args
    except ValueError as e:
        raise ValueError(f"Некорректный ввод: {str(e)}")


def parse_column_definitions(column_args: List[str]) -> List[Tuple[str, str]]:
    """Parse column definitions like 'name:str' into (name, type) tuples."""
    columns = []
    for arg in column_args:
        if ':' not in arg:
            raise ValueError(f"Некорректное определение столбца: {arg}")
        
        name, col_type = arg.split(':', 1)
        if not name or not col_type:
            raise ValueError(f"Некорректное определение столбца: {arg}")
        
        columns.append((name.strip(), col_type.strip()))
    
    return columns