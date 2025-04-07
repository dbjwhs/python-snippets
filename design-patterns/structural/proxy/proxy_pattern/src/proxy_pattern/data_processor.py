# MIT License
# Copyright (c) 2025 dbjwhs

"""Data Processor implementation for Proxy pattern demo."""

import os
from abc import ABC, abstractmethod
from typing import final

from proxy_pattern.logger import Logger, LogLevel


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