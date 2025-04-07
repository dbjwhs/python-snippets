# MIT License
# Copyright (c) 2025 dbjwhs

"""Proxy Design Pattern Implementation in Python."""

from proxy_pattern.proxy import (
    DataProcessorProxy,
    IDataProcessor,
    Logger,
    LogLevel,
    RealDataProcessor,
    main,
    read_file_to_list,
    run_file_tests,
    run_vector_tests,
)

__all__ = [
    "IDataProcessor",
    "RealDataProcessor", 
    "DataProcessorProxy",
    "Logger",
    "LogLevel",
    "read_file_to_list",
    "run_vector_tests",
    "run_file_tests",
    "main"
]