# MIT License
# Copyright (c) 2025 dbjwhs

"""Logger implementation for Proxy pattern demo."""

from enum import Enum, auto
from typing import ClassVar, Optional

from icecream import ic  # type: ignore


class LogLevel(Enum):
    """Log levels for the logger."""
    
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    DEBUG = auto()


class Logger:
    """A simple singleton logger implementation."""
    
    _instance: ClassVar[Optional["Logger"]] = None
    
    def __init__(self) -> None:
        """Initialize the logger."""
        if Logger._instance is not None:
            raise RuntimeError("Logger instance already exists, use getInstance() instead")
        self._enable_icecream = True
    
    @classmethod
    def get_instance(cls) -> "Logger":
        """Get the singleton instance of the logger.
        
        Returns:
            Logger: The singleton logger instance
        """
        if cls._instance is None:
            cls._instance = Logger()
        return cls._instance

    def log(self, level: LogLevel, message: str) -> None:
        """Log a message with the specified log level.
        
        Args:
            level: The log level for the message
            message: The message to log
        """
        # Always use icecream, but configure differently based on settings
        if not self._enable_icecream:
            # Save current config
            old_prefix = ic.prefix
            old_output_function = ic.outputFunction
            
            # Configure for simple output without the ic| prefix
            ic.configureOutput(prefix='')
            
            # Log the message
            ic(f"[{level.name}] {message}")
            
            # Restore original config
            ic.configureOutput(prefix=old_prefix, outputFunction=old_output_function)
        else:
            # Normal icecream logging
            ic(f"[{level.name}] {message}")