# MIT License
# Copyright (c) 2025 dbjwhs

"""Tests for the data processor classes."""

import os
import tempfile
import unittest
from unittest.mock import patch

from proxy_pattern.data_processor import DataProcessorProxy, RealDataProcessor, read_file_to_list


class TestRealDataProcessor(unittest.TestCase):
    """Tests for the RealDataProcessor class."""

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