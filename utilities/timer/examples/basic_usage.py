#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""Basic usage example for HighResolutionTimer."""

import time

from timer_py import HighResolutionTimer


def complex_operation() -> None:
    """Simulate a complex operation by sleeping for 100ms."""
    time.sleep(0.1)


def operation_1() -> None:
    """Simulate operation 1 by sleeping for 50ms."""
    time.sleep(0.05)


def operation_2() -> None:
    """Simulate operation 2 by sleeping for 75ms."""
    time.sleep(0.075)


def main() -> None:
    """Run the basic usage example."""
    print("HighResolutionTimer Basic Usage Example")
    print("======================================\n")

    timer = HighResolutionTimer()

    # Basic timing
    print("Basic timing example:")
    timer.start()
    complex_operation()
    timer.stop()

    # Get results in different formats
    print(f"Raw nanoseconds: {timer.elapsed_nanoseconds()}")
    print(f"Formatted time: {timer.elapsed_formatted()}")

    # Check timer status
    if not timer.running():
        print("Timer is stopped")

    # Multiple measurements
    print("\nMultiple measurements example:")
    timer.reset()
    timer.start()
    operation_1()
    print(f"Time so far: {timer.elapsed_formatted()}")
    operation_2()
    timer.stop()
    print(f"Final time: {timer.elapsed_formatted()}")


if __name__ == "__main__":
    main()
