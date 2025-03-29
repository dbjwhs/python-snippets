# MIT License
# Copyright (c) 2025 dbjwhs

"""Tests for the HighResolutionTimer class."""

import time
from unittest import mock

from timer_py import HighResolutionTimer


class TestHighResolutionTimer:
    """Test suite for the HighResolutionTimer class."""

    def test_initial_state(self) -> None:
        """Test that the timer is initialized with correct default values."""
        timer = HighResolutionTimer()
        assert not timer.running()
        assert timer.elapsed_seconds() == 0.0
        assert timer.elapsed_nanoseconds() == 0.0
        assert timer.elapsed_microseconds() == 0.0
        assert timer.elapsed_milliseconds() == 0.0

    def test_start_stop(self) -> None:
        """Test starting and stopping the timer."""
        timer = HighResolutionTimer()
        timer.start()
        assert timer.running()
        time.sleep(0.01)  # Small delay
        timer.stop()
        assert not timer.running()
        assert timer.elapsed_seconds() > 0.0

    def test_reset(self) -> None:
        """Test resetting the timer."""
        timer = HighResolutionTimer()
        timer.start()
        time.sleep(0.01)  # Small delay
        timer.stop()
        elapsed = timer.elapsed_seconds()
        assert elapsed > 0.0

        timer.reset()
        assert not timer.running()
        assert timer.elapsed_seconds() == 0.0

    def test_multiple_measurements(self) -> None:
        """Test multiple start/stops."""
        timer = HighResolutionTimer()

        # First measurement
        timer.start()
        time.sleep(0.01)
        timer.stop()
        first_elapsed = timer.elapsed_seconds()

        # Second measurement
        timer.start()
        time.sleep(0.02)
        timer.stop()
        second_elapsed = timer.elapsed_seconds()

        # Second measurement should be different from the first
        assert second_elapsed > 0.0
        assert abs(second_elapsed - first_elapsed) > 0.001  # At least 1ms difference

    def test_elapsed_while_running(self) -> None:
        """Test getting elapsed time while timer is running."""
        timer = HighResolutionTimer()
        timer.start()
        time.sleep(0.01)
        running_elapsed = timer.elapsed_seconds()
        assert running_elapsed > 0.0
        timer.stop()
        stopped_elapsed = timer.elapsed_seconds()
        assert stopped_elapsed >= running_elapsed

    def test_elapsed_formatted(self) -> None:
        """Test the elapsed_formatted method with different time ranges."""
        timer = HighResolutionTimer()
        
        # Test with different values by mocking _get_elapsed_seconds
        
        # Nanoseconds range (less than 1 microsecond)
        with mock.patch.object(timer, "_get_elapsed_seconds", return_value=500e-9):
            assert "ns" in timer.elapsed_formatted()
        
        # Microseconds range (less than 1 millisecond)
        with mock.patch.object(timer, "_get_elapsed_seconds", return_value=500e-6):
            assert "µs" in timer.elapsed_formatted()
        
        # Milliseconds range (less than 1 second)
        with mock.patch.object(timer, "_get_elapsed_seconds", return_value=500e-3):
            assert "ms" in timer.elapsed_formatted()
        
        # Seconds range (1 second or more)
        with mock.patch.object(timer, "_get_elapsed_seconds", return_value=5.0):
            assert "s" in timer.elapsed_formatted()

    def test_conversion_factors(self) -> None:
        """Test the conversion factors between different time units."""
        timer = HighResolutionTimer()

        # Mock a fixed elapsed time (1 second)
        with mock.patch.object(timer, "_get_elapsed_seconds", return_value=1.0):
            assert timer.elapsed_seconds() == 1.0
            assert timer.elapsed_milliseconds() == 1000.0
            assert timer.elapsed_microseconds() == 1000000.0
            assert timer.elapsed_nanoseconds() == 1000000000.0
