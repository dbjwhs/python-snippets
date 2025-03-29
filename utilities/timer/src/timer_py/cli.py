# MIT License
# Copyright (c) 2025 dbjwhs

"""Command-line interface for the timer package."""

import time

from icecream import ic

from timer_py.timer import HighResolutionTimer


def run_basic_demo() -> None:
    """Run a basic demonstration of the timer functionality."""
    print("High Resolution Timer Demo")
    print("=========================\n")

    # Initialize timer
    timer = HighResolutionTimer()

    # Test 1: Basic timing
    print("Test 1: Basic timing with microseconds delay")
    timer.start()
    time.sleep(0.0005)  # 500 microseconds
    timer.stop()
    print(f"Elapsed time: {timer.elapsed_formatted()}\n")

    # Test 2: Different time units
    print("Test 2: Display time in different units")
    timer.start()
    time.sleep(0.1)  # 100 milliseconds
    timer.stop()
    print(f"Nanoseconds:  {timer.elapsed_nanoseconds():.2f} ns")
    print(f"Microseconds: {timer.elapsed_microseconds():.2f} µs")
    print(f"Milliseconds: {timer.elapsed_milliseconds():.2f} ms")
    print(f"Seconds:      {timer.elapsed_seconds():.5f} s")
    print(f"Formatted:    {timer.elapsed_formatted()}\n")

    # Test 3: Timer status
    print("Test 3: Timer status checking")
    timer.reset()
    print(f"After reset, timer running: {'yes' if timer.running() else 'no'}")
    timer.start()
    print(f"After start, timer running: {'yes' if timer.running() else 'no'}")
    timer.stop()
    print(f"After stop, timer running: {'yes' if timer.running() else 'no'}\n")

    # Test 4: Measuring while running
    print("Test 4: Measuring while timer is running")
    timer.start()
    print("Starting measurement...")
    for ndx in range(1, 4):
        time.sleep(0.1)  # 100 milliseconds
        print(f"Time at check {ndx}: {timer.elapsed_formatted()}")
    timer.stop()
    print(f"Final time: {timer.elapsed_formatted()}\n")

    # Test 5: Multiple start/stops
    print("Test 5: Multiple start/stops")
    timer.reset()
    timer.start()
    time.sleep(0.1)  # 100 milliseconds
    timer.stop()
    print(f"First measurement: {timer.elapsed_formatted()}")

    # Start a new measurement
    timer.start()
    time.sleep(0.2)  # 200 milliseconds
    timer.stop()
    print(f"Second measurement: {timer.elapsed_formatted()}")


def main() -> None:
    """Execute the main CLI functionality."""
    # Configure icecream for debugging
    ic.configureOutput(prefix="Debug | ")

    # Disable icecream for normal usage
    ic.disable()

    # Run demo
    run_basic_demo()


if __name__ == "__main__":
    main()
