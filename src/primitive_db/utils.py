import json
import os
from typing import Any, Dict, List

from .constants import DATA_DIR, META_FILE


def ensure_data_dir() -> None:
    """Создает директорию для данных, если она не существует."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def save_metadata(metadata: Dict[str, Any]) -> None:
    """Сохраняет метаданные базы данных."""
    ensure_data_dir()
    with open(os.path.join(DATA_DIR, META_FILE), 'w') as f:
        json.dump(metadata, f, indent=2)


def load_metadata() -> Dict[str, Any]:
    """Загружает метаданные базы данных."""
    try:
        with open(os.path.join(DATA_DIR, META_FILE), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tables": {}}


def save_table_data(table_name: str, data: List[Dict[str, Any]]) -> None:
    """Сохраняет данные таблицы в отдельный JSON-файл."""
    ensure_data_dir()
    filename = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def load_table_data(table_name: str) -> List[Dict[str, Any]]:
    """Загружает данные таблицы из JSON-файла."""
    try:
        filename = os.path.join(DATA_DIR, f"{table_name}.json")
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def table_exists(table_name: str) -> bool:
    """Проверяет существование таблицы."""
    metadata = load_metadata()
    return table_name in metadata["tables"]


def get_table_file_path(table_name: str) -> str:
    """Возвращает путь к файлу таблицы."""
    return os.path.join(DATA_DIR, f"{table_name}.json")


def get_next_id(table_data: List[Dict[str, Any]]) -> int:
    """Генерирует следующий ID для таблицы."""
    if not table_data:
        return 1
    return max(item.get("ID", 0) for item in table_data) + 1
