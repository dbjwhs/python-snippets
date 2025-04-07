# MIT License
# Copyright (c) 2025 dbjwhs

"""Implementation of the Proxy design pattern.

The proxy pattern, introduced by the Gang of Four in 1994, provides a surrogate or
placeholder for another object to control access to it. It belongs to the structural
pattern family and is widely used in modern software development.

Historical context:
- Originated in early distributed systems for managing remote resources
- Gained prominence with the rise of object-oriented programming
- Evolved to handle modern concerns like lazy loading and access control

Real-world applications:
1. Virtual proxy (lazy loading):
   - Loading large images in web browsers
   - Database connection pooling
   - Loading heavy documents in word processors

2. Protection proxy (access control):
   - Corporate network access management
   - Cloud service authentication layers
   - Database query permissions

3. Remote proxy:
   - Microservices communication
   - Distributed system interfaces
   - REST API gateways

4. Logging proxy:
   - System activity monitoring
   - Audit trails in financial systems
   - Debug logging in production systems

This implementation demonstrates a protection proxy with logging capabilities,
commonly used in enterprise systems where access control and audit trails are
crucial. The pattern is particularly relevant in:
- Financial transaction systems
- Healthcare record management
- Enterprise resource planning (ERP) systems
- Cloud-based service interfaces

Class hierarchy:
- IDataProcessor (interface)
  - RealDataProcessor: Performs actual data processing
  - DataProcessorProxy: Controls access to RealDataProcessor

Key relationships:
- Proxy forwards authenticated requests to real processor
- Proxy maintains ownership of real processor
- Both derived classes implement IDataProcessor interface
- Proxy adds authentication and logging without modifying real processor
"""

import os
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import ClassVar, Optional, final

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
            raise RuntimeError("Logger instance already exists, use get_instance() instead")
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


class IDataProcessor(ABC):
    """Interface for both a real subject and proxy."""
    
    @abstractmethod
    def process_data(self, data: list[str]) -> None:
        """Process the given data.
        
        Args:
            data: The data to process
        """
        pass
    
    @abstractmethod
    def get_processed_count(self) -> int:
        """Get the total number of items processed.
        
        Returns:
            int: The count of processed items
        """
        pass


@final
class RealDataProcessor(IDataProcessor):
    """Real subject class that does the actual work."""
    
    def __init__(self) -> None:
        """Initialize the real data processor."""
        self._processed_count: int = 0
    
    def process_data(self, data: list[str]) -> None:
        """Process the given data and track the count.
        
        Args:
            data: The data to process
        """
        self._processed_count += len(data)
        
        # Log processing activity
        Logger.get_instance().log(
            LogLevel.INFO,
            f"Processing {len(data)} items in real processor"
        )
        
        # Simulate processing
        for item in data:
            Logger.get_instance().log(LogLevel.INFO, f"Processing item: {item}")
    
    def get_processed_count(self) -> int:
        """Get the number of items processed.
        
        Returns:
            int: The count of processed items
        """
        return self._processed_count


@final
class DataProcessorProxy(IDataProcessor):
    """Proxy class that adds access control and logging."""
    
    def __init__(self) -> None:
        """Initialize the data processor proxy."""
        self._real_processor: RealDataProcessor = RealDataProcessor()
        self._is_authenticated: bool = False
        self._access_count: int = 0
    
    def authenticate(self) -> None:
        """Authenticate the proxy to allow access to the real processor."""
        self._is_authenticated = True
        Logger.get_instance().log(LogLevel.INFO, "Proxy: Authentication successful")
    
    def process_data(self, data: list[str]) -> None:
        """Process the given data if authenticated.
        
        Args:
            data: The data to process
        """
        self._access_count += 1
        
        # Check authentication before allowing access
        if not self._is_authenticated:
            Logger.get_instance().log(LogLevel.INFO, "Proxy: Access denied - not authenticated")
            return
        
        # Log proxy access
        Logger.get_instance().log(
            LogLevel.INFO,
            f"Proxy: Forwarding {len(data)} items to real processor"
        )
        
        # Forward request to real processor
        self._real_processor.process_data(data)
    
    def get_processed_count(self) -> int:
        """Get the number of items processed by the real processor.
        
        Returns:
            int: The count of processed items
        """
        return self._real_processor.get_processed_count()
    
    def get_access_count(self) -> int:
        """Get the number of access attempts to this proxy.
        
        Returns:
            int: The count of access attempts
        """
        return self._access_count


def read_file_to_list(filename: str) -> list[str]:
    """Read a file into a list of strings (one per line).
    
    Args:
        filename: The path to the file to read
        
    Returns:
        List[str]: The lines from the file
        
    Raises:
        FileNotFoundError: If the file couldn't be opened
    """
    # Convert relative path to absolute for testing files
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
    full_path = os.path.join(project_root, filename)
    
    try:
        with open(full_path, encoding="utf-8") as file:
            lines = file.readlines()
            # Remove trailing newlines
            lines = [line.rstrip("\n") for line in lines]
            
        Logger.get_instance().log(
            LogLevel.INFO,
            f"Read {len(lines)} lines from file: {filename}"
        )
        return lines
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Failed to open file: {filename}") from e


def run_vector_tests() -> None:
    """Run tests using vector data with the Proxy pattern."""
    Logger.get_instance().log(LogLevel.INFO, "Starting vector<string> tests")

    proxy = DataProcessorProxy()
    test_data: list[str] = ["item1", "item2", "item3"]

    # Test 1: Unauthenticated access
    Logger.get_instance().log(LogLevel.INFO, "Test 1: Attempting unauthenticated access")
    proxy.process_data(test_data)
    assert proxy.get_processed_count() == 0
    assert proxy.get_access_count() == 1

    # Test 2: Authenticated access
    Logger.get_instance().log(LogLevel.INFO, "Test 2: Attempting authenticated access")
    proxy.authenticate()
    proxy.process_data(test_data)
    assert proxy.get_processed_count() == 3
    assert proxy.get_access_count() == 2

    # Test 3: Multiple processing calls
    Logger.get_instance().log(LogLevel.INFO, "Test 3: Testing multiple processing calls")
    proxy.process_data(test_data)
    assert proxy.get_processed_count() == 6
    assert proxy.get_access_count() == 3

    Logger.get_instance().log(LogLevel.INFO, "Vector<string> tests completed successfully")


def run_file_tests(file1: str, file2: str) -> None:
    """Run tests using file data with the Proxy pattern.
    
    Args:
        file1: Path to the first file to process
        file2: Path to the second file to process
    """
    Logger.get_instance().log(LogLevel.INFO, "Starting file tests")

    proxy = DataProcessorProxy()

    # Test 1: Read and process original file
    Logger.get_instance().log(LogLevel.INFO, "Test 1: Processing original file")
    original_data = read_file_to_list(file1)

    # Authenticate and process
    proxy.authenticate()
    proxy.process_data(original_data)

    # Verify processing
    assert proxy.get_processed_count() == len(original_data)
    assert proxy.get_access_count() == 1

    # Test 2: Compare processing of both files
    Logger.get_instance().log(LogLevel.INFO, "Test 2: Comparing file processing")
    altered_data = read_file_to_list(file2)

    # Process altered file
    proxy.process_data(altered_data)

    # Verify cumulative processing
    assert proxy.get_processed_count() == len(original_data) + len(altered_data)
    assert proxy.get_access_count() == 2

    # Test 3: Process files multiple times to ensure consistent behavior
    Logger.get_instance().log(LogLevel.INFO, "Test 3: Testing multiple file processing")
    proxy.process_data(original_data)
    proxy.process_data(altered_data)

    # Verify final counts
    assert proxy.get_processed_count() == 2 * (len(original_data) + len(altered_data))
    assert proxy.get_access_count() == 4

    Logger.get_instance().log(LogLevel.INFO, "File tests completed successfully")


def main() -> None:
    """Run main demonstration of the Proxy pattern."""
    try:
        # Run vector tests
        run_vector_tests()
        
        # Skip file tests as they require specific files
        Logger.get_instance().log(
            LogLevel.INFO,
            "Skipping file tests - please run with proper files if needed"
        )
        
        Logger.get_instance().log(LogLevel.INFO, "All tests completed successfully")
    except Exception as e:
        Logger.get_instance().log(LogLevel.INFO, f"Error during testing: {str(e)}")


if __name__ == "__main__":
    main()