# MIT License
# Copyright (c) 2025 dbjwhs

"""Example using the Proxy pattern with vector data."""


from proxy_pattern.data_processor import DataProcessorProxy
from proxy_pattern.logger import Logger, LogLevel


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