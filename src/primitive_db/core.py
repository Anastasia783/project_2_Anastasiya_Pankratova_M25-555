from typing import Dict, Any, List, Tuple
from .constants import VALID_TYPES
from .utils import delete_table_file
from .decorators import handle_db_errors


@handle_db_errors
def create_table(metadata: Dict[str, Any], table_name: str, columns: List[Tuple[str, str]]) -> Dict[str, Any]:
    """Create a new table with the given name and columns."""
    # Check if table already exists
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')
    
    # Validate column types
    for col_name, col_type in columns:
        if col_type not in VALID_TYPES:
            raise ValueError(f'Некорректный тип данных: {col_type}. Допустимые типы: {", ".join(VALID_TYPES)}')
    
    # Add ID column automatically
    table_columns = [("ID", "int")] + columns
    
    # Create table metadata
    metadata[table_name] = {
        "columns": table_columns,
        "next_id": 1
    }
    
    # Create empty data file
    from .utils import save_table_data
    save_table_data(table_name, [])
    
    return metadata


@handle_db_errors
def drop_table(metadata: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    """Drop an existing table."""
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')
    
    # Remove from metadata
    del metadata[table_name]
    
    # Delete data file
    delete_table_file(table_name)
    
    return metadata


def list_tables(metadata: Dict[str, Any]) -> List[str]:
    """List all tables in the database."""
    return list(metadata.keys())


def get_table_columns(metadata: Dict[str, Any], table_name: str) -> List[Tuple[str, str]]:
    """Get column definitions for a table."""
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')
    
    return metadata[table_name]["columns"]


def format_columns_display(columns: List[Tuple[str, str]]) -> str:
    """Format columns for display."""
    return ", ".join([f"{name}:{type}" for name, type in columns])