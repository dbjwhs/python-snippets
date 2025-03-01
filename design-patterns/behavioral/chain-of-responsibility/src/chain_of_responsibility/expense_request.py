# MIT License
# Copyright (c) 2025 dbjwhs

"""Expense request implementation for the Chain of Responsibility pattern."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExpenseRequest:
    """Dataclass representing an expense request.
    
    Attributes:
        amount: The monetary amount of the expense
        purpose: The reason for the expense
    """

    amount: float
    purpose: str