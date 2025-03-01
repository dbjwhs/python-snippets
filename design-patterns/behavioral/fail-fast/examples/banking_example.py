# MIT License
# Copyright (c) 2025 dbjwhs

"""
Example usage of the Fail-Fast pattern in a banking application.

This example demonstrates how to use the FailFastAccount class to implement
fail-fast validation in a banking context.
"""

from icecream import ic

from fail_fast import FailFastAccount


def run_banking_example() -> None:
    """
    Run a demonstration of the Fail-Fast pattern in a banking application.
    """
    ic.configureOutput(prefix="Banking Demo | ")
    
    # Create a new account
    try:
        ic("Creating a new account for Jane Doe")
        account = FailFastAccount("Jane Doe")
        
        # Perform some operations
        ic("Making initial deposit")
        account.deposit(5000.0)
        ic(f"Current balance: ${account.balance:.2f}")
        
        ic("Withdrawing money for monthly expenses")
        account.withdraw(1500.0)
        ic(f"Remaining balance: ${account.balance:.2f}")
        
        # Show fail-fast behavior with invalid operations
        ic("Attempting invalid operations to demonstrate fail-fast:")
        
        try:
            ic("Trying to withdraw negative amount")
            account.withdraw(-200.0)
        except ValueError as e:
            ic(f"Error caught: {e}")
            
        try:
            ic("Trying to withdraw more than allowed")
            account.withdraw(10000.0)
        except RuntimeError as e:
            ic(f"Error caught: {e}")
            
        # Close the account
        ic("Closing the account")
        account.close_account()
        
        # Try to perform operation on closed account
        try:
            ic("Trying to deposit after account closure")
            account.deposit(100.0)
        except RuntimeError as e:
            ic(f"Error caught: {e}")
            
        ic("Example completed!")
        
    except Exception as e:
        ic(f"Unexpected error: {e}")


if __name__ == "__main__":
    run_banking_example()