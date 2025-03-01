# MIT License
# Copyright (c) 2025 dbjwhs

"""
Test module for the fail_fast pattern implementation.
"""

import pytest

from fail_fast import FailFastAccount


class TestFailFastAccount:
    """
    Test suite for the FailFastAccount class implementing the Fail-Fast pattern.
    """
    
    def test_valid_account_creation(self) -> None:
        """Test that a valid account can be created."""
        account = FailFastAccount("John Doe")
        assert account.account_holder == "John Doe"
        assert account.balance == 0.0
        assert account.is_active
        
    def test_invalid_account_creation(self) -> None:
        """Test that creating an account with an empty holder name fails."""
        with pytest.raises(ValueError, match="Account holder name cannot be empty"):
            FailFastAccount("")
            
    def test_valid_deposit(self) -> None:
        """Test that a valid deposit increases the balance."""
        account = FailFastAccount("John Doe")
        deposit_amount = 1000.0
        account.deposit(deposit_amount)
        assert account.balance == deposit_amount
        
    def test_invalid_deposit(self) -> None:
        """Test that depositing a negative or zero amount fails."""
        account = FailFastAccount("John Doe")
        with pytest.raises(ValueError, match="Deposit amount must be positive"):
            account.deposit(-100.0)
        with pytest.raises(ValueError, match="Deposit amount must be positive"):
            account.deposit(0.0)
            
    def test_valid_withdrawal(self) -> None:
        """Test that a valid withdrawal decreases the balance."""
        account = FailFastAccount("John Doe")
        deposit_amount = 1000.0
        withdrawal_amount = 500.0
        account.deposit(deposit_amount)
        account.withdraw(withdrawal_amount)
        assert account.balance == (deposit_amount - withdrawal_amount)
        
    def test_invalid_withdrawal_amount(self) -> None:
        """Test that withdrawing a negative or zero amount fails."""
        account = FailFastAccount("John Doe")
        with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
            account.withdraw(-100.0)
        with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
            account.withdraw(0.0)
            
    def test_insufficient_funds(self) -> None:
        """Test that withdrawing more than allowed fails."""
        account = FailFastAccount("John Doe")
        account.deposit(500.0)
        with pytest.raises(RuntimeError, match="Insufficient funds"):
            account.withdraw(2000.0)
            
    def test_account_closure(self) -> None:
        """Test that an account can be closed."""
        account = FailFastAccount("John Doe")
        account.close_account()
        assert not account.is_active
        
    def test_operations_on_closed_account(self) -> None:
        """Test that operations on a closed account fail."""
        account = FailFastAccount("John Doe")
        account.close_account()
        
        with pytest.raises(RuntimeError, match="Account is inactive"):
            account.deposit(100.0)
            
        with pytest.raises(RuntimeError, match="Account is inactive"):
            account.withdraw(100.0)
            
        with pytest.raises(RuntimeError, match="Account is inactive"):
            _ = account.balance
            
        with pytest.raises(RuntimeError, match="Account is inactive"):
            _ = account.account_holder
            
    def test_double_closure(self) -> None:
        """Test that closing an already closed account fails."""
        account = FailFastAccount("John Doe")
        account.close_account()
        with pytest.raises(RuntimeError, match="Account already inactive"):
            account.close_account()