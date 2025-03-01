# MIT License
# Copyright (c) 2025 dbjwhs

"""
Fail-Fast pattern implementation in Python.

This module implements the Fail-Fast pattern which immediately reports
and handles invalid states or operations, preventing cascading failures.
"""

from typing import Final

from icecream import ic


class FailFastAccount:
    """
    Fail-fast pattern implementation that validates state immediately.
    Throws exceptions for invalid states to prevent cascading failures.
    
    This class demonstrates the pattern in a banking context with
    comprehensive state validation and immediate error reporting.
    """

    def __init__(self, account_holder: str) -> None:
        """
        Constructor enforcing initial valid state.
        
        Args:
            account_holder: The name of the account holder
            
        Raises:
            ValueError: If account holder name is empty
        """
        if not account_holder:
            ic("Failed to create account: Empty account holder name")
            raise ValueError("Account holder name cannot be empty")
            
        self._balance: float = 0.0
        self._account_holder: str = account_holder
        self._minimum_balance: Final[float] = -1000.0
        self._is_active: bool = True
        
        ic(f"Account created for: {account_holder}")
        
    def _validate_state(self) -> None:
        """
        Validates if the account is in a valid state for operations.
        
        Raises:
            RuntimeError: If account is inactive or has invalid holder name
        """
        if not self._is_active:
            ic("Account validation failed: Account is inactive")
            raise RuntimeError("Account is inactive")
            
        if not self._account_holder:
            ic("Account validation failed: Invalid account holder")
            raise RuntimeError("Invalid account holder")
    
    def deposit(self, amount: float) -> None:
        """
        Deposit money into account, fails fast on invalid amount.
        
        Args:
            amount: The amount to deposit
            
        Raises:
            ValueError: If amount is not positive
            RuntimeError: If account is in an invalid state
        """
        self._validate_state()
        
        if amount <= 0:
            ic(f"Invalid deposit amount: {amount}")
            raise ValueError("Deposit amount must be positive")
            
        self._balance += amount
        ic(f"Deposited ${amount:.2f}, new balance: ${self._balance:.2f}")
    
    def withdraw(self, amount: float) -> None:
        """
        Withdraw money from an account, fails fast on invalid amount or insufficient funds.
        
        Args:
            amount: The amount to withdraw
            
        Raises:
            ValueError: If amount is not positive
            RuntimeError: If insufficient funds or account is in an invalid state
        """
        self._validate_state()
        
        if amount <= 0:
            ic(f"Invalid withdrawal amount: {amount}")
            raise ValueError("Withdrawal amount must be positive")
            
        if (self._balance - amount) < self._minimum_balance:
            ic(f"Insufficient funds: balance=${self._balance:.2f}, "
               f"withdrawal=${amount:.2f}, minimum=${self._minimum_balance:.2f}")
            raise RuntimeError("Insufficient funds")
            
        self._balance -= amount
        ic(f"Withdrawn ${amount:.2f}, new balance: ${self._balance:.2f}")
    
    def close_account(self) -> None:
        """
        Close account, fails fast if already closed.
        
        Raises:
            RuntimeError: If account is already inactive
        """
        if not self._is_active:
            ic("Cannot close already inactive account")
            raise RuntimeError("Account already inactive")
            
        self._is_active = False
        ic(f"Account closed for: {self._account_holder}")
    
    @property
    def balance(self) -> float:
        """
        Get the current account balance.
        
        Returns:
            float: The current balance
            
        Raises:
            RuntimeError: If account is in an invalid state
        """
        self._validate_state()
        return self._balance
    
    @property
    def account_holder(self) -> str:
        """
        Get the account holder's name.
        
        Returns:
            str: The account holder's name
            
        Raises:
            RuntimeError: If account is in an invalid state
        """
        self._validate_state()
        return self._account_holder
    
    @property
    def is_active(self) -> bool:
        """
        Check if the account is active.
        
        Returns:
            bool: True if account is active, False otherwise
        """
        return self._is_active