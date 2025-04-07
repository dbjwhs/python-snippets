#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the basic Proxy pattern example.

This script runs a simple demonstration of the Proxy pattern
showing authentication and access control.
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from proxy_pattern.proxy import Logger, LogLevel, DataProcessorProxy
    
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
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Make sure you've installed the package with 'uv pip install -e .'")
    sys.exit(1)