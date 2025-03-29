"""Tests for barrier example implementations."""

import threading
from unittest.mock import Mock, call

import pytest

from barrier_example.examples import CustomBarrierExample, ModernBarrierExample


class TestBarrierExamples:
    """Test suite for barrier example implementations."""

    @pytest.mark.parametrize("example_class", [CustomBarrierExample, ModernBarrierExample])
    def test_example_demonstration(self, example_class) -> None:
        """Test that example demonstrations run without errors.

        Args:
            example_class: The example class to test.
        """
        # Create a mock logger
        mock_logger = Mock()

        # Run the demonstration with a small number of threads
        num_threads = 2
        example_class.demonstrate(num_threads, mock_logger)

        # Verify the logger was called at least once per thread
        assert mock_logger.log.call_count >= num_threads

    def test_worker_behavior_custom(self) -> None:
        """Test the behavior of the CustomBarrierExample worker."""
        # Create mocks
        mock_barrier = Mock()
        mock_logger = Mock()

        # Create a thread to run the worker
        thread = threading.Thread(
            target=CustomBarrierExample.worker, args=(mock_barrier, 1, mock_logger)
        )
        thread.start()
        thread.join(timeout=3.0)  # Set a timeout for test stability

        # Verify the barrier was called exactly 3 times (for 3 phases)
        assert mock_barrier.wait.call_count == 3

        # Verify logger was called with appropriate messages
        expected_calls = [
            call("CustomBarrierExample Thread 1 completed phase 1"),
            call("CustomBarrierExample Thread 1 starting phase 2"),
            call("CustomBarrierExample Thread 1 completed phase 2"),
            call("CustomBarrierExample Thread 1 starting phase 3"),
            call("CustomBarrierExample Thread 1 completed phase 3"),
            call("CustomBarrierExample Thread 1 starting phase 4"),
        ]
        mock_logger.log.assert_has_calls(expected_calls)

    def test_worker_behavior_modern(self) -> None:
        """Test the behavior of the ModernBarrierExample worker."""
        # Create mocks
        mock_barrier = Mock()
        mock_logger = Mock()

        # Create a thread to run the worker
        thread = threading.Thread(
            target=ModernBarrierExample.worker, args=(mock_barrier, 2, mock_logger)
        )
        thread.start()
        thread.join(timeout=3.0)  # Set a timeout for test stability

        # Verify the barrier was called exactly 3 times (for 3 phases)
        assert mock_barrier.wait.call_count == 3

        # Verify logger was called with appropriate messages
        expected_calls = [
            call("Thread 2 completed phase 1"),
            call("Thread 2 starting phase 2"),
            call("Thread 2 completed phase 2"),
            call("Thread 2 starting phase 3"),
            call("Thread 2 completed phase 3"),
            call("Thread 2 starting phase 4"),
        ]
        mock_logger.log.assert_has_calls(expected_calls)
