#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Tests for the thread pool implementation.
"""

import concurrent.futures
import time
from threading import Event

import pytest

from thread_pool.thread_pool import Logger, ThreadPool


class TestThreadPool:
    """Test cases for ThreadPool class."""

    @pytest.fixture
    def logger(self) -> Logger:
        """Logger fixture."""
        return Logger.get_instance()

    @pytest.fixture
    def thread_pool(self, logger: Logger) -> ThreadPool:
        """ThreadPool fixture with 4 threads."""
        pool = ThreadPool(4, logger)
        yield pool
        pool.shutdown()

    def test_enqueue_and_get_result(self, thread_pool: ThreadPool) -> None:
        """Test enqueuing a task and getting its result."""
        # Enqueue a task that returns the square of a number
        future = thread_pool.enqueue(lambda x: x * x, 5)
        
        # Get the result
        result = future.result()
        
        # Verify the result
        assert result == 25

    def test_enqueue_multiple_tasks(self, thread_pool: ThreadPool) -> None:
        """Test enqueuing multiple tasks and getting all results."""
        # Enqueue 10 tasks
        futures: list[concurrent.futures.Future[int]] = []
        for i in range(10):
            future = thread_pool.enqueue(lambda x: x * x, i)
            futures.append(future)
        
        # Get and verify all results
        for i, future in enumerate(futures):
            assert future.result() == i * i

    def test_task_exception_propagation(self, thread_pool: ThreadPool) -> None:
        """Test that exceptions in tasks are properly propagated."""
        # Enqueue a task that raises an exception
        future = thread_pool.enqueue(lambda: 1/0)
        
        # Verify that the exception is raised when getting the result
        with pytest.raises(ZeroDivisionError):
            future.result()

    def test_enqueue_after_shutdown(self, logger: Logger) -> None:
        """Test that enqueuing after shutdown raises an exception."""
        # Create and immediately shut down a thread pool
        pool = ThreadPool(1, logger)
        pool.shutdown()
        
        # Verify that enqueuing after shutdown raises an exception
        with pytest.raises(RuntimeError):
            pool.enqueue(lambda: 42)

    def test_concurrent_task_execution(self, thread_pool: ThreadPool) -> None:
        """Test that tasks are executed concurrently."""
        # Create an event to signal when all tasks are running
        running_event = Event()
        # Create an event to signal when tasks should complete
        complete_event = Event()
        
        # Counter to track how many tasks are running concurrently
        running_count = 0
        max_running = 0
        
        def task() -> int:
            nonlocal running_count, max_running
            
            # Increment the running count and update max_running
            running_count += 1
            max_running = max(max_running, running_count)
            
            # If at least 3 tasks are running, signal that we're running concurrently
            if running_count >= 3:
                running_event.set()
            
            # Wait for the signal to complete
            complete_event.wait()
            
            # Decrement the running count
            running_count -= 1
            
            return max_running
        
        # Enqueue 4 tasks
        futures = [thread_pool.enqueue(task) for _ in range(4)]
        
        # Wait for tasks to start running concurrently (timeout after 2 seconds)
        assert running_event.wait(2.0), "Tasks did not start concurrently"
        
        # Signal tasks to complete
        complete_event.set()
        
        # Get results and verify that at least 3 tasks ran concurrently
        results = [future.result() for future in futures]
        assert max(results) >= 3

    def test_perform_real_work(self, thread_pool: ThreadPool) -> None:
        """Test thread pool with a more realistic workload."""
        def compute_intensive_task(n: int) -> int:
            """A computation-intensive task."""
            # Simulate computation with sleep
            time.sleep(0.1)
            result = 0
            for i in range(n):
                result += i * i
            return result
        
        # Expected results for inputs 0 to 9
        expected_results = [sum(i * i for i in range(n)) for n in range(10)]
        
        # Enqueue 10 tasks with different inputs
        futures = [thread_pool.enqueue(compute_intensive_task, n) for n in range(10)]
        
        # Get and verify results
        for i, future in enumerate(futures):
            assert future.result() == expected_results[i]

    def test_thread_pool_stress(self, thread_pool: ThreadPool) -> None:
        """Stress test with many quick tasks."""
        # Number of tasks to enqueue
        task_count = 100
        
        # Enqueue many small tasks
        futures = [thread_pool.enqueue(lambda i=i: i, i) for i in range(task_count)]
        
        # Verify all results
        for i, future in enumerate(futures):
            assert future.result() == i