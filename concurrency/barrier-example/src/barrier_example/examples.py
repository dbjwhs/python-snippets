"""Example implementations using barrier pattern.

This module provides example implementations of the barrier pattern:
1. CustomBarrierExample - Using the custom barrier implementation
2. ModernBarrierExample - Using Python's threading.Barrier
"""

import random
import threading
import time
from dataclasses import dataclass
from typing import Protocol, final

from icecream import ic

from barrier_example.barrier import CustomBarrier, ModernBarrier


class Logger(Protocol):
    """Protocol for logging functionality."""

    def log(self, *args: object) -> None:
        """Log a message.

        Args:
            *args: The message components to log.
        """
        ...


@dataclass
class IceCreamLogger:
    """Logger implementation using icecream."""

    @staticmethod
    def log(*args: object) -> None:
        """Log a message using icecream.

        Args:
            *args: The message components to log.
        """
        ic(*args)


@final
class CustomBarrierExample:
    """Example using the custom barrier implementation."""

    @staticmethod
    def worker(barrier: CustomBarrier, worker_id: int, logger: Logger) -> None:
        """Worker function for the custom barrier example.

        Args:
            barrier: The barrier to synchronize on.
            worker_id: The ID of the worker thread.
            logger: The logger to use for output.
        """
        for phase in range(1, 4):
            # Simulate some work
            sleep_time = random.randint(100, 1000) / 1000
            time.sleep(sleep_time)

            logger.log(f"CustomBarrierExample Thread {worker_id} completed phase {phase}")

            # Wait for all threads at the barrier
            barrier.wait()
            logger.log(f"CustomBarrierExample Thread {worker_id} starting phase {phase + 1}")

    @staticmethod
    def demonstrate(num_threads: int, logger: Logger) -> None:
        """Demonstrate the custom barrier implementation.

        Args:
            num_threads: The number of threads to use.
            logger: The logger to use for output.
        """
        barrier = CustomBarrier(num_threads)
        threads = []

        logger.log("\nDemonstrating custom barrier implementation:")

        # Create threads
        for ndx in range(num_threads):
            thread = threading.Thread(
                target=CustomBarrierExample.worker, args=(barrier, ndx, logger)
            )
            threads.append(thread)
            thread.start()

        # Join threads
        for thread in threads:
            thread.join()


@final
class ModernBarrierExample:
    """Example using the modern barrier implementation."""

    @staticmethod
    def worker(barrier: ModernBarrier, worker_id: int, logger: Logger) -> None:
        """Worker function for the modern barrier example.

        Args:
            barrier: The barrier to synchronize on.
            worker_id: The ID of the worker thread.
            logger: The logger to use for output.
        """
        for phase in range(1, 4):
            # Simulate some work
            sleep_time = random.randint(100, 1000) / 1000
            time.sleep(sleep_time)

            logger.log(f"Thread {worker_id} completed phase {phase}")

            # Wait for all threads at the barrier
            barrier.wait()

            logger.log(f"Thread {worker_id} starting phase {phase + 1}")

    @staticmethod
    def demonstrate(num_threads: int, logger: Logger) -> None:
        """Demonstrate the modern barrier implementation.

        Args:
            num_threads: The number of threads to use.
            logger: The logger to use for output.
        """
        logger.log("Demonstrating modern barrier implementation:")
        barrier = ModernBarrier(num_threads)
        threads = []

        # Create threads
        for ndx in range(num_threads):
            thread = threading.Thread(
                target=ModernBarrierExample.worker, args=(barrier, ndx, logger)
            )
            threads.append(thread)
            thread.start()

        # Join threads
        for thread in threads:
            thread.join()
