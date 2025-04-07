# MIT License
# Copyright (c) 2025 dbjwhs

"""Basic example of the Proxy design pattern.

Shows a simple example of the proxy pattern with authentication
and access control functionality.
"""

from proxy_pattern import DataProcessorProxy, Logger, LogLevel


def main() -> None:
    """Run a basic example of the proxy pattern."""
    # Get logger instance
    logger = Logger.get_instance()
    
    # Create the proxy
    proxy = DataProcessorProxy()
    
    # Define some data to process
    data = ["Record 1", "Record 2", "Record 3", "Record 4"]
    
    # Attempt to process data without authentication
    logger.log(LogLevel.INFO, "Attempting to process data without authentication...")
    proxy.process_data(data)
    logger.log(LogLevel.INFO, f"Processed count: {proxy.get_processed_count()}")
    logger.log(LogLevel.INFO, f"Access count: {proxy.get_access_count()}")
    
    # Authenticate the proxy
    logger.log(LogLevel.INFO, "Authenticating proxy...")
    proxy.authenticate()
    
    # Process data after authentication
    logger.log(LogLevel.INFO, "Attempting to process data after authentication...")
    proxy.process_data(data)
    logger.log(LogLevel.INFO, f"Processed count: {proxy.get_processed_count()}")
    logger.log(LogLevel.INFO, f"Access count: {proxy.get_access_count()}")


if __name__ == "__main__":
    main()