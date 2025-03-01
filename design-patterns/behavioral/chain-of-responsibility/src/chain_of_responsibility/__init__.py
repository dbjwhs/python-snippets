# MIT License
# Copyright (c) 2025 dbjwhs

"""
Chain of Responsibility Design Pattern implementation in Python.

This package provides a flexible implementation of the Chain of Responsibility pattern
where requests are passed along a chain of handlers until one handles it.
"""

from .expense_handler import (
    CEO,
    Crom,
    DepartmentManager,
    Director,
    ExpenseHandler,
    TeamLeader,
)
from .expense_request import ExpenseRequest
from .logger import LogLevel, Logger

__all__ = [
    "ExpenseHandler",
    "TeamLeader",
    "DepartmentManager",
    "Director",
    "CEO",
    "Crom",
    "ExpenseRequest",
    "Logger",
    "LogLevel",
]