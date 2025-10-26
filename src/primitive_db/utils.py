"""Utility functions for file operations."""

import json
import os
from typing import Any, Dict
from .constants import META_FILE, DATA_DIR


def ensure_data_dir() -> None:
    """Ensure data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_metadata() -> Dict[str, Any]:
    """Load database metadata from file."""
    try:
        with open(META_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(metadata: Dict[str, Any]) -> None:
    """Save database metadata to file."""
    with open(META_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)


def load_table_data(table_name: str) -> list:
    """Load table data from file."""
    file_path = os.path.join(DATA_DIR, f"{table_name}.json")
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name: str, data: list) -> None:
    """Save table data to file."""
    ensure_data_dir()
    file_path = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)