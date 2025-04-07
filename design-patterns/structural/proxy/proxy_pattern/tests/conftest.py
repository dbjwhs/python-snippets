# MIT License
# Copyright (c) 2025 dbjwhs

"""Pytest configuration for the Proxy pattern tests."""

import os
import sys

import pytest

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


@pytest.fixture(autouse=True)
def reset_logger() -> None:
    """Reset the Logger singleton before each test."""
    from proxy_pattern.proxy import Logger
    Logger._instance = None