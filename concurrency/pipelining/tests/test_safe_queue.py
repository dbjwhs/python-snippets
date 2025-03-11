# MIT License
# Copyright (c) 2025 dbjwhs

"""Tests for the SafeQueue class."""

import threading
import time
import pytest
from typing import List

import sys
sys.path.append('/Users/dbjones/ng/dbjwhs/python-snippets/concurrency/pipelining')
from src.pipeline.safe_queue import SafeQueue


def test_push_pop() -> None:
    """Test basic push and pop operations."""
    queue: SafeQueue[int] = SafeQueue()
    
    # Push a value
    queue.push(42)
    
    # Pop the value
    result_container: list = [None]
    success = queue.pop(result_container)
    
    assert success
    assert result_container[0] == 42


def test_empty_queue() -> None:
    """Test behavior with an empty queue."""
    queue: SafeQueue[int] = SafeQueue()
    
    # Check if empty
    assert queue.is_empty()
    
    # Set done and try to pop
    queue.set_done()
    result_container: list = [None]
    success = queue.pop(result_container)
    
    assert not success


def test_multiple_values() -> None:
    """Test pushing and popping multiple values."""
    queue: SafeQueue[int] = SafeQueue()
    
    # Push multiple values
    for i in range(5):
        queue.push(i)
    
    # Pop all values
    results: List[int] = []
    for _ in range(5):
        val_container: list = [None]
        queue.pop(val_container)
        results.append(val_container[0])
    
    assert results == [0, 1, 2, 3, 4]


def test_concurrent_access() -> None:
    """Test concurrent access to the queue."""
    queue: SafeQueue[int] = SafeQueue()
    result_queue: SafeQueue[int] = SafeQueue()
    
    # Producer thread function
    def producer() -> None:
        for i in range(100):
            queue.push(i)
            time.sleep(0.001)  # Small sleep to ensure interleaving
        queue.set_done()
    
    # Consumer thread function
    def consumer() -> None:
        val_container: list = [None]
        while queue.pop(val_container):
            result_queue.push(val_container[0])
        result_queue.set_done()
    
    # Start producer and consumer threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for threads to finish
    producer_thread.join()
    consumer_thread.join()
    
    # Collect results
    results: List[int] = []
    val_container: list = [None]
    while result_queue.pop(val_container):
        results.append(val_container[0])
    
    # Check that all values were processed
    assert len(results) == 100
    assert sorted(results) == list(range(100))