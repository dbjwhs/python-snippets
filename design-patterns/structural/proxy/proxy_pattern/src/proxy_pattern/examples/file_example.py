# MIT License
# Copyright (c) 2025 dbjwhs

"""Example using the Proxy pattern with file data."""

from proxy_pattern.data_processor import DataProcessorProxy, read_file_to_list
from proxy_pattern.logger import Logger, LogLevel


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