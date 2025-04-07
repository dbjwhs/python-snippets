# MIT License
# Copyright (c) 2025 dbjwhs

"""Tests for the Proxy pattern implementation."""

import os
import tempfile
import unittest
from unittest.mock import patch

from proxy_pattern.proxy import (
    DataProcessorProxy,
    Logger,
    LogLevel,
    RealDataProcessor,
    read_file_to_list,
)


class TestRealDataProcessor(unittest.TestCase):
    """Tests for the RealDataProcessor class."""

    def setUp(self) -> None:
        """Reset the logger singleton before each test."""
        Logger._instance = None

    def test_process_data(self) -> None:
        """Test that data is processed correctly."""
        processor = RealDataProcessor()
        data: list[str] = ["item1", "item2", "item3"]
        
        processor.process_data(data)
        self.assertEqual(processor.get_processed_count(), 3)
        
        # Process more data
        processor.process_data(["item4", "item5"])
        self.assertEqual(processor.get_processed_count(), 5)


class TestDataProcessorProxy(unittest.TestCase):
    """Tests for the DataProcessorProxy class."""

    def setUp(self) -> None:
        """Reset the logger singleton before each test."""
        Logger._instance = None

    def test_unauthenticated_access(self) -> None:
        """Test that unauthenticated access is denied."""
        proxy = DataProcessorProxy()
        data: list[str] = ["item1", "item2", "item3"]
        
        proxy.process_data(data)
        self.assertEqual(proxy.get_processed_count(), 0)
        self.assertEqual(proxy.get_access_count(), 1)

    def test_authenticated_access(self) -> None:
        """Test that authenticated access is allowed."""
        proxy = DataProcessorProxy()
        data: list[str] = ["item1", "item2", "item3"]
        
        proxy.authenticate()
        proxy.process_data(data)
        self.assertEqual(proxy.get_processed_count(), 3)
        self.assertEqual(proxy.get_access_count(), 1)

    def test_multiple_access(self) -> None:
        """Test multiple access attempts."""
        proxy = DataProcessorProxy()
        data: list[str] = ["item1", "item2"]
        
        # First attempt - unauthenticated
        proxy.process_data(data)
        self.assertEqual(proxy.get_processed_count(), 0)
        self.assertEqual(proxy.get_access_count(), 1)
        
        # Authenticate
        proxy.authenticate()
        
        # Second attempt - authenticated
        proxy.process_data(data)
        self.assertEqual(proxy.get_processed_count(), 2)
        self.assertEqual(proxy.get_access_count(), 2)
        
        # Third attempt - authenticated with different data
        proxy.process_data(["item3", "item4", "item5"])
        self.assertEqual(proxy.get_processed_count(), 5)
        self.assertEqual(proxy.get_access_count(), 3)


class TestFileUtils(unittest.TestCase):
    """Tests for the file utility functions."""

    def setUp(self) -> None:
        """Reset the logger singleton before each test."""
        Logger._instance = None

    def test_read_file_to_list(self) -> None:
        """Test reading a file into a list of strings."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write("line1\nline2\nline3\n")
            temp_path = temp_file.name
        
        try:
            # Mock the path resolution to use our temp file
            with patch('os.path.join', return_value=temp_path):
                lines = read_file_to_list("dummy_path")
                self.assertEqual(lines, ["line1", "line2", "line3"])
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)

    def test_file_not_found(self) -> None:
        """Test that a FileNotFoundError is raised when the file doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            read_file_to_list("nonexistent_file.txt")


class TestLogger(unittest.TestCase):
    """Tests for the Logger class."""

    def setUp(self) -> None:
        """Reset the singleton instance before each test."""
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