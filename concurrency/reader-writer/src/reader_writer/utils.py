# MIT License
# Copyright (c) 2025 dbjwhs

"""
Utility functions and classes for the reader_writer package.

This module contains common utilities used across the reader_writer package,
including logging and thread management utilities.
"""

import random
import threading
from enum import Enum, auto
from threading import Lock
from typing import ClassVar, Final, Optional

from icecream import ic


class LogLevel(Enum):
    """Log levels for the logger."""
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    DEBUG = auto()


class Logger:
    """Thread-safe singleton logger using icecream."""
    _instance: ClassVar[Optional["Logger"]] = None
    _lock: ClassVar[Lock] = Lock()

    def __new__(cls) -> "Logger":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self) -> None:
        """Initialize the logger instance."""
        self._mutex: Lock = Lock()

    @classmethod
    def get_instance(cls) -> "Logger":
        """Get the singleton instance of the logger."""
        if cls._instance is None:
            return cls()
        return cls._instance

    def log(self, level: LogLevel, message: str) -> None:
        """Log a message with the specified log level."""
        with self._mutex:
            if level == LogLevel.INFO:
                ic(f"INFO: {message}")
            elif level == LogLevel.WARNING:
                ic(f"WARNING: {message}")
            elif level == LogLevel.ERROR:
                ic(f"ERROR: {message}")
            elif level == LogLevel.DEBUG:
                ic(f"DEBUG: {message}")


class NonCopyable:
    """Mixin class to prevent instances from being copied."""
    
    def __init__(self) -> None:
        pass
        
    def __copy__(self) -> None:
        error_msg = "Copying of this object is not allowed"
        raise TypeError(error_msg)
        
    def __deepcopy__(self, memo: dict) -> None:
        error_msg = "Deep copying of this object is not allowed"
        raise TypeError(error_msg)


def thread_id_to_string() -> str:
    """Convert the current thread ID to a string."""
    return str(threading.get_ident())


class RandomGenerator:
    """Generate random numbers within a specified range."""
    
    def __init__(self, min_val: int, max_val: int) -> None:
        """Initialize the random generator with a range."""
        self.min_val: Final[int] = min_val
        self.max_val: Final[int] = max_val
        
    def get_number(self) -> int:
        """Get a random number within the specified range."""
        return random.randint(self.min_val, self.max_val)