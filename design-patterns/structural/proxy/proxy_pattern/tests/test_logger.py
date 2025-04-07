# MIT License
# Copyright (c) 2025 dbjwhs

"""Tests for the logger implementation."""

import unittest

from proxy_pattern.logger import Logger, LogLevel


class TestLogger(unittest.TestCase):
    """Tests for the Logger class."""

    def setUp(self) -> None:
        """Reset the singleton instance before each test."""
        # Reset the singleton instance
        Logger._instance = None
    
    def test_singleton_pattern(self) -> None:
        """Test that the Logger follows the singleton pattern."""
        logger1 = Logger.get_instance()
        logger2 = Logger.get_instance()
        self.assertIs(logger1, logger2)
    
    def test_direct_initialization_error(self) -> None:
        """Test that direct initialization raises an error if instance exists."""
        Logger.get_instance()  # Create an instance
        with self.assertRaises(RuntimeError):
            Logger()  # Attempt to create another instance directly
    
    def test_log_with_icecream(self) -> None:
        """Test logging with icecream enabled works without errors."""
        logger = Logger.get_instance()
        logger._enable_icecream = True
        
        # Just verify it doesn't raise an exception
        try:
            logger.log(LogLevel.INFO, "Test message")
        except Exception as e:
            self.fail(f"logger.log() raised {type(e).__name__} unexpectedly!")
    
    def test_log_without_icecream(self) -> None:
        """Test logging with icecream disabled works without errors."""
        logger = Logger.get_instance()
        logger._enable_icecream = False
        
        # Just verify it doesn't raise an exception
        try:
            logger.log(LogLevel.ERROR, "Error message")
        except Exception as e:
            self.fail(f"logger.log() raised {type(e).__name__} unexpectedly!")


class TestLogLevel(unittest.TestCase):
    """Tests for the LogLevel enum."""
    
    def test_log_levels(self) -> None:
        """Test that all expected log levels are present."""
        self.assertTrue(hasattr(LogLevel, "INFO"))
        self.assertTrue(hasattr(LogLevel, "WARNING"))
        self.assertTrue(hasattr(LogLevel, "ERROR"))
        self.assertTrue(hasattr(LogLevel, "DEBUG"))