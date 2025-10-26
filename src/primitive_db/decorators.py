"""Decorators for the database system."""

import time
from functools import wraps
from typing import Any, Callable


def handle_db_errors(func: Callable) -> Callable:
    """Handle database-related errors."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (FileNotFoundError, KeyError, ValueError, TypeError) as e:
            return f"Error: {str(e)}"
    return wrapper


def confirm_action(action: str) -> Callable:
    """Decorator factory for confirming actions."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # In a real implementation, we would ask for confirmation
            # For now, we'll just log the action
            print(f"Confirming action: {action}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time(func: Callable) -> Callable:
    """Log the execution time of a function."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.4f} seconds")
        return result
    return wrapper


def cache_results(max_size: int = 128) -> Callable:
    """Cache decorator with max size limit."""
    def decorator(func: Callable) -> Callable:
        cache = {}
        keys = []
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = str(args) + str(kwargs)
            
            if key in cache:
                return cache[key]
            
            result = func(*args, **kwargs)
            
            # Manage cache size
            if len(keys) >= max_size:
                oldest_key = keys.pop(0)
                del cache[oldest_key]
            
            cache[key] = result
            keys.append(key)
            
            return result
        return wrapper
    return decorator