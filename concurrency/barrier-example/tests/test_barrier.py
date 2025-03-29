"""Tests for barrier implementations."""

import threading
import time

import pytest

from typing import Any

from barrier_example.barrier import CustomBarrier, ModernBarrier


class TestBarrierImplementations:
    """Test suite for barrier implementations."""

    @pytest.mark.parametrize("barrier_class", [CustomBarrier, ModernBarrier])
    def test_barrier_synchronization(self, barrier_class: Any) -> None:
        """Test that barriers correctly synchronize threads.

        Args:
            barrier_class: The barrier class to test.
        """
        num_threads = 4
        barrier = barrier_class(num_threads)
        results: list[int] = []
        release_phase2 = threading.Event()

        def worker(worker_id: int) -> None:
            """Worker thread function.

            Args:
                worker_id: The ID of the worker thread.
            """
            # Phase 1: Add the thread ID
            results.append(worker_id)
            # Wait for all threads to reach this point
            barrier.wait()

            # Phase 2: Only proceed when told to
            if worker_id == 0:
                # Thread 0 waits a bit to ensure other threads are waiting
                time.sleep(0.1)
                release_phase2.set()
            release_phase2.wait()
            # Wait at barrier again
            barrier.wait()

        # Create and start threads
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(num_threads)]
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify that all threads reached phase 1
        assert sorted(results) == list(range(num_threads))

    @pytest.mark.parametrize("barrier_class", [CustomBarrier, ModernBarrier])
    def test_barrier_reset(self, barrier_class: Any) -> None:
        """Test that barriers correctly reset after all threads arrive.

        Args:
            barrier_class: The barrier class to test.
        """
        num_threads = 3
        phases = 3
        barrier = barrier_class(num_threads)
        phase_counts = [0] * phases

        def worker() -> None:
            """Worker thread function."""
            for phase in range(phases):
                # Increment count for current phase
                phase_counts[phase] += 1
                # Wait for all threads
                barrier.wait()

        # Create and start threads
        threads = [threading.Thread(target=worker) for _ in range(num_threads)]
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check that all phases completed with the correct number of threads
        for phase in range(phases):
            assert phase_counts[phase] == num_threads
