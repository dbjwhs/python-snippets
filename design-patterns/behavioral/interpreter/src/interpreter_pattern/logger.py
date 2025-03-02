# MIT License
# Copyright (c) 2025 dbjwhs

"""Logger module for the Interpreter pattern implementation."""

from enum import Enum

from icecream import ic


class LogLevel(Enum):
    """Log level enumeration."""
    
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class Logger:
    """Singleton logger class for the Interpreter pattern implementation."""
    
    _instance: "Logger | None" = None

    def __init__(self):
        """Initialize a Logger instance."""
        self._level = LogLevel.INFO

    def __new__(cls) -> "Logger":
        """Create a new Logger instance or return the existing one."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance
    
    @staticmethod
    def get_instance() -> "Logger":
        """Get the Logger singleton instance."""
        if Logger._instance is None:
            return Logger()
        
        # Ensure logger is properly initialized
        if not hasattr(Logger._instance, "_level") or Logger._instance._level is None:
            Logger._instance._init()
            
        return Logger._instance
    
    def _init(self) -> None:
        """Initialize the logger."""
        self._level = LogLevel.INFO
        # Configure icecream to use a cleaner output format
        ic.configureOutput(prefix="", includeContext=False, outputFunction=print)
    
    def set_level(self, level: LogLevel) -> None:
        """Set the log level.
        
        Args:
            level: The log level to set.
        """
        self._level = level
    
    def log(self, level: LogLevel, message: str, *args: object) -> None:
        """Log a message at the specified level.
        
        Args:
            level: The log level.
            message: The message to log.
            *args: Additional arguments to format the message.
        """
        if level.value >= self._level.value:
            formatted_message = message.format(*args) if args else message
            prefix = f"[{level.name}] "
            # Using icecream's ic() directly to show expression values
            ic.configureOutput(prefix=prefix)
            ic(formatted_message)
            # Reset to default configuration
            ic.configureOutput(prefix="")
    
    def log_with_depth(self, level: LogLevel, depth: int, message: str) -> None:
        """Log a message with indentation based on depth.
        
        Args:
            level: The log level.
            depth: The indentation depth.
            message: The message to log.
        """
        if level.value >= self._level.value:
            indent = "  " * depth
            prefix = f"[{level.name}] {indent}"
            # Using icecream's ic() with custom prefix that includes indentation
            ic.configureOutput(prefix=prefix)
            ic(message)
            # Reset to default configuration
            ic.configureOutput(prefix="")