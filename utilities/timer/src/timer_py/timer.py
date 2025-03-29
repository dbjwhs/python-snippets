# MIT License
# Copyright (c) 2025 dbjwhs

"""High resolution timer module."""

import time
from dataclasses import dataclass, field
from enum import Enum, auto

from icecream import ic

NANO_SECOND = 1e9

class TimeUnit(Enum):
    """Time unit enumeration."""

    NANOSECONDS = auto()
    MICROSECONDS = auto()
    MILLISECONDS = auto()
    SECONDS = auto()


@dataclass
class HighResolutionTimer:
    """
    A high-resolution timer class for precise time measurements.

    This class provides a simple interface for measuring elapsed time
    with high precision. It supports multiple time units and automatic
    formatting with appropriate units.
    """

    _start_time: float | None = field(default=None, init=False)
    _end_time: float | None = field(default=None, init=False)
    _is_running: bool = field(default=False, init=False)

    def start(self) -> None:
        """Start the timer."""
        self._start_time = time.perf_counter_ns() / NANO_SECOND
        self._is_running = True
        ic("Timer started")

    def stop(self) -> None:
        """Stop the timer if it's currently running."""
        if self._is_running:
            self._end_time = time.perf_counter_ns() / NANO_SECOND
            self._is_running = False
            ic("Timer stopped")

    def reset(self) -> None:
        """Reset the timer to its initial state."""
        self._start_time = None
        self._end_time = None
        self._is_running = False
        ic("Timer reset")

    def _get_elapsed_seconds(self) -> float:
        """
        Get the elapsed time in seconds.

        Returns:
            float: The elapsed time in seconds.
        """
        if not self._start_time:
            return 0.0

        if not self._is_running:
            if not self._end_time:
                return 0.0
            return self._end_time - self._start_time

        current_time = time.perf_counter_ns() / NANO_SECOND
        return current_time - self._start_time

    def elapsed_nanoseconds(self) -> float:
        """
        Get elapsed time in nanoseconds.

        Returns:
            float: The elapsed time in nanoseconds.
        """
        return self._get_elapsed_seconds() * NANO_SECOND

    def elapsed_microseconds(self) -> float:
        """
        Get elapsed time in microseconds.

        Returns:
            float: The elapsed time in microseconds.
        """
        return self._get_elapsed_seconds() * 1e6

    def elapsed_milliseconds(self) -> float:
        """
        Get elapsed time in milliseconds.

        Returns:
            float: The elapsed time in milliseconds.
        """
        return self._get_elapsed_seconds() * 1e3

    def elapsed_seconds(self) -> float:
        """
        Get elapsed time in seconds.

        Returns:
            float: The elapsed time in seconds.
        """
        return self._get_elapsed_seconds()

    def elapsed_formatted(self) -> str:
        """
        Get formatted string of elapsed time with the appropriate unit.

        Returns:
            str: Formatted elapsed time with unit.
        """
        elapsed = self.elapsed_nanoseconds()

        if elapsed < 1000.0:
            return f"{elapsed:.3f} ns"
        elif elapsed < 1000000.0:
            return f"{elapsed / 1000.0:.3f} µs"
        elif elapsed < 1000000000.0:
            return f"{elapsed / 1000000.0:.3f} ms"
        else:
            return f"{elapsed / 1000000000.0:.3f} s"

    def running(self) -> bool:
        """
        Check if the timer is currently running.

        Returns:
            bool: True if the timer is running, False otherwise.
        """
        return self._is_running
