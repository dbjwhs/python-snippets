# MIT License
# Copyright (c) 2025 dbjwhs

import threading
from copy import copy, deepcopy
from unittest.mock import patch

import pytest

from reader_writer.utils import Logger, LogLevel, NonCopyable, RandomGenerator, thread_id_to_string


def test_logger_singleton():
    """Test that the Logger class implements the singleton pattern."""
    logger1 = Logger.get_instance()
    logger2 = Logger.get_instance()
    assert logger1 is logger2, "Multiple logger instances were created"


def test_logger_log_levels():
    """Test that the Logger class handles all log levels."""
    logger = Logger.get_instance()
    
    # Test each log level to ensure no exceptions
    with patch('reader_writer.utils.ic') as mock_ic:
        logger.log(LogLevel.INFO, "Info message")
        logger.log(LogLevel.WARNING, "Warning message")
        logger.log(LogLevel.ERROR, "Error message")
        logger.log(LogLevel.DEBUG, "Debug message")
        
        expected_calls = 4  # One for each log level
        assert mock_ic.call_count == expected_calls, "Expected calls to ic for each log level"


def test_non_copyable():
    """Test that NonCopyable class prevents copying and deep copying."""
    class TestClass(NonCopyable):
        def __init__(self):
            super().__init__()
            self.value = 42
    
    instance = TestClass()
    
    # Test that copying raises TypeError
    with pytest.raises(TypeError):
        copy(instance)
    
    # Test that deep copying raises TypeError
    with pytest.raises(TypeError):
        deepcopy(instance)


def test_thread_id_to_string():
    """Test that thread_id_to_string returns the current thread ID as a string."""
    thread_id = thread_id_to_string()
    assert isinstance(thread_id, str), "Thread ID should be a string"
    assert thread_id == str(threading.get_ident()), "Thread ID doesn't match current thread"


def test_random_generator():
    """Test that RandomGenerator produces numbers within the specified range."""
    min_val = 1
    max_val = 10
    generator = RandomGenerator(min_val, max_val)
    
    # Test multiple random numbers
    for _ in range(100):
        number = generator.get_number()
        assert min_val <= number <= max_val, f"Generated {number} outside range {min_val}-{max_val}"