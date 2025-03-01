# MIT License
# Copyright (c) 2025 dbjwhs

"""Logger implementation for the Chain of Responsibility pattern."""

from enum import Enum, auto
from typing import Final


class LogLevel(Enum):
    """Enumeration of log levels."""

    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    DEBUG = auto()


class Logger:
    """Singleton logger class for the application.
    
    This class provides a simple logging mechanism that mimics the C++ Logger
    used in the original implementation.
    """

    _instance = None

    def __new__(cls) -> "Logger":
        """Create a new Logger instance if one doesn't exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> "Logger":
        """Get the singleton instance of the Logger."""
        return cls.__new__(cls)

    def log(self, level: LogLevel, message: str) -> None:
        """Log a message with the specified log level.
        
        Args:
            level: The log level for the message
            message: The message to log
        """
        level_str: Final[str] = f"[{level.name}]"
        print(f"{level_str:<10} {message}")