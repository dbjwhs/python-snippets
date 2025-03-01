# MIT License
# Copyright (c) 2025 dbjwhs

"""
Main module entry point for the fail_fast package.

This module demonstrates the Fail-Fast pattern by running a series of
tests on the FailFastAccount class.
"""

from icecream import ic

from .fail_fast import FailFastAccount


def main() -> None:
    """
    Run a demonstration of the Fail-Fast pattern implementation.
    """
    try:
        ic("Starting Fail-Fast Pattern tests")

        # Test 1: Valid account creation
        account = FailFastAccount("John Doe")
        assert account.account_holder == "John Doe"
        assert account.balance == 0.0
        assert account.is_active

        # Test 2: Invalid account creation
        try:
            _ = FailFastAccount("")
            raise AssertionError("Should have thrown exception")
        except ValueError as e:
            ic("Test passed: Empty account holder name rejected", e)

        # Test 3: Valid deposit
        deposit_amount = 1000.0
        account.deposit(deposit_amount)
        assert account.balance == deposit_amount

        # Test 4: Invalid deposit
        try:
            account.deposit(-100.0)
            raise AssertionError("Should have thrown exception")
        except ValueError as e:
            ic("Test passed: Negative deposit rejected", e)

        # Test 5: Valid withdrawal
        withdrawal_amount = 500.0
        account.withdraw(withdrawal_amount)
        assert account.balance == (deposit_amount - withdrawal_amount)

        # Test 6: Withdrawal exceeding minimum balance
        try:
            account.withdraw(2000.0)
            raise AssertionError("Should have thrown exception")
        except RuntimeError as e:
            ic("Test passed: Excessive withdrawal rejected", e)

        # Test 7: Account closure
        account.close_account()
        assert not account.is_active

        # Test 8: Operations on closed account
        try:
            account.deposit(100.0)
            # This line should never be reached, but is here for completeness
            ic("ERROR: deposit on closed account succeeded")  # pragma: no cover
            raise AssertionError("Should have thrown exception")
        except RuntimeError as e:
            ic("Test passed: Operation on closed account rejected", e)

        # Test 9: Double closure
        try:
            account.close_account()
            raise AssertionError("Should have thrown exception")
        except RuntimeError as e:
            ic("Test passed: Double closure rejected", e)

        ic("All tests completed successfully")

    except Exception as e:
        ic(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()