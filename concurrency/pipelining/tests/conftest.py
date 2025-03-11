# MIT License
# Copyright (c) 2025 dbjwhs

"""Pytest fixtures for the pipeline tests."""

import sys
import pytest
from typing import Generator

# Add project root to path
sys.path.append('/Users/dbjones/ng/dbjwhs/python-snippets')

# Import the logger
from headers.project_utils import Logger

@pytest.fixture
def logger() -> Logger:
    """
    Provide a logger instance for tests.
    
    Returns:
        Logger: A configured logger instance
    """
    return Logger.getInstance()