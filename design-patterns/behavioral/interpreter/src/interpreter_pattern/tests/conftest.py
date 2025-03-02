# MIT License
# Copyright (c) 2025 dbjwhs

"""Test configuration module for the interpreter pattern tests."""

import pytest

from interpreter_pattern.context import Context
from interpreter_pattern.logger import Logger
from interpreter_pattern.logger import LogLevel


@pytest.fixture
def setup_logger() -> Logger:
    """Set up the logger for testing.
    
    Returns:
        The logger instance.
    """
    logger = Logger.get_instance()
    # Set to DEBUG level to test all log messages
    logger.set_level(LogLevel.DEBUG)
    return logger


@pytest.fixture
def context() -> Context:
    """Create a new context for testing.
    
    Returns:
        A new context instance.
    """
    return Context()