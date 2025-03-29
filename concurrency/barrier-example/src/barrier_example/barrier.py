"""Barrier implementations in Python.

This module provides two barrier implementations:
1. CustomBarrier - Manual implementation using locks and condition variables
2. ModernBarrier - Using Python's threading.Barrier
"""

from threading import Barrier as ThreadingBarrier
from threading import Condition, Lock
from typing import Protocol, final


class BarrierProtocol(Protocol):
    """Protocol defining the interface for barrier implementations."""

    def wait(self) -> None:
        """Wait at the barrier until all threads have arrived."""
        ...


@final
class CustomBarrier:
    """Custom implementation of a barrier using locks and conditions.

    This class provides functionality similar to threading.Barrier but is
    implemented manually to demonstrate the underlying mechanics.
    """

    def __init__(self, count: int) -> None:
        """Initialize the barrier with a thread count.

        Args:
            count: Number of threads that must call wait() before any may proceed.
        """
        self._thread_count: int = count
        self._counter: int = count
        self._waiting: int = 0
        self._lock: Lock = Lock()
        self._condition: Condition = Condition(self._lock)
        self._phase: bool = False

    def wait(self) -> None:
        """Wait at the barrier until all threads have arrived.

        The first n-1 threads calling this method will block until the nth thread
        calls the method. Then all threads will be released and the barrier resets.
        """
        with self._condition:
            phase_copy = self._phase

            if self._counter == 1:
                # Last thread to arrive
                self._counter = self._thread_count
                self._waiting = self._thread_count - 1
                self._phase = not self._phase
                self._condition.notify_all()
            else:
                # Not the last thread, need to wait
                self._counter -= 1
                self._waiting += 1

                # Wait for the phase to change, protecting against spurious wakeups
                self._condition.wait_for(lambda: phase_copy != self._phase)

                self._waiting -= 1


@final
class ModernBarrier:
    """Modern barrier implementation using Python's threading.Barrier.

    This is a thin wrapper around threading.Barrier to maintain API compatibility
    with CustomBarrier while leveraging the standard library implementation.
    """

    def __init__(self, count: int) -> None:
        """Initialize the barrier with a thread count.

        Args:
            count: Number of threads that must call wait() before any may proceed.
        """
        self._barrier: ThreadingBarrier = ThreadingBarrier(count)

    def wait(self) -> None:
        """Wait at the barrier until all threads have arrived.

        This method delegates to the threading.Barrier's wait method.
        """
        self._barrier.wait()
