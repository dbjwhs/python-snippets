# MIT License
# Copyright (c) 2025 dbjwhs

from enum import Enum, auto
from typing import Optional
import threading
from icecream import ic


class LogLevel(Enum):
    """Logging levels similar to standard logging libraries."""
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class Logger:
    """Thread-safe logger implementation using icecream."""
    _instance: Optional['Logger'] = None
    _lock = threading.Lock()

    def __new__(cls) -> 'Logger':
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance._init_logger()
            return cls._instance

    def _init_logger(self) -> None:
        """Initialize the logger instance."""
        self._mutex = threading.Lock()
        # Configure icecream
        ic.configureOutput(prefix='', includeContext=True)

    @staticmethod
    def getInstance() -> 'Logger':
        """Get the singleton instance of the logger."""
        return Logger()

    def log(self, level: LogLevel, message: str) -> None:
        """
        Log a message with the specified log level.
        
        Args:
            level: The log level of the message
            message: The message to log
        """
        with self._mutex:
            prefix = f"[{level.name}] "
            ic(f"{prefix}{message}")

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.log(LogLevel.DEBUG, message)

    def info(self, message: str) -> None:
        """Log an info message."""
        self.log(LogLevel.INFO, message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.log(LogLevel.WARNING, message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self.log(LogLevel.ERROR, message)

    def critical(self, message: str) -> None:
        """Log a critical message."""
        self.log(LogLevel.CRITICAL, message)