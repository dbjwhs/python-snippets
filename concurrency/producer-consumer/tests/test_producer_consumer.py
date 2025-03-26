# MIT License
# Copyright (c) 2025 dbjwhs

"""
Tests for the producer-consumer implementation.

These tests verify the thread-safety and correctness of the Producer-Consumer implementation.
"""

import threading
import time
from unittest.mock import patch

import pytest

from producer_consumer.producer_consumer import Consumer, Producer, ThreadSafeQueue


class TestThreadSafeQueue:
    """Test class for ThreadSafeQueue functionality."""

    def test_empty_and_size(self):
        """Test that a new queue is empty and reports correct size after operations."""
        queue = ThreadSafeQueue[int](5)
        assert queue.empty()
        assert queue.size() == 0

        queue.push(1)
        assert not queue.empty()
        assert queue.size() == 1

        queue.pop()
        assert queue.empty()
        assert queue.size() == 0

    def test_push_and_pop(self):
        """Test that items pushed to the queue can be popped in FIFO order."""
        queue = ThreadSafeQueue[int](5)
        values = [1, 2, 3, 4, 5]
        
        for val in values:
            queue.push(val)
        
        popped = []
        while not queue.empty():
            popped.append(queue.pop())
        
        assert popped == values

    def test_max_capacity(self):
        """
        Test that the queue blocks when it reaches maximum capacity.
        
        This test uses a separate thread to push items to the queue until it reaches
        capacity, then verifies that the thread is blocked until an item is popped.
        """
        queue = ThreadSafeQueue[int](2)
        
        # Event to signal when pushing thread is blocked
        block_event = threading.Event()
        
        # Flag to track if pushing thread completed
        push_completed = [False]
        
        def push_items():
            queue.push(1)
            queue.push(2)
            # This should block
            block_event.set()
            # We don't want to use a timeout here, so we use a longer timeout
            queue.push(3)
            push_completed[0] = True
        
        push_thread = threading.Thread(target=push_items)
        push_thread.start()
        
        # Wait for the pushing thread to block
        block_event.wait(timeout=1.0)
        time.sleep(0.1)  # Give a bit more time for the thread to block
        
        assert queue.size() == 2
        assert not push_completed[0]  # The thread should be blocked
        
        # Unblock the thread by popping an item
        queue.pop()
        
        # Wait for the thread to complete
        push_thread.join(timeout=1.0)
        
        assert push_completed[0]
        assert queue.size() == 2


class TestProducerConsumer:
    """Test class for Producer and Consumer functionality."""
    
    @patch('random.randint')
    def test_producer(self, mock_randint):
        """Test that the producer pushes values to the queue."""
        mock_randint.return_value = 42
        
        queue = ThreadSafeQueue[int](5)
        running = threading.Event()
        running.set()
        
        producer = Producer(queue, running, 1, delay=0.01)
        
        # Run producer in a thread for a short time
        producer_thread = threading.Thread(target=producer)
        producer_thread.start()
        time.sleep(0.05)  # Allow time for a few productions
        running.clear()
        producer_thread.join()
        
        # Verify items were produced
        assert not queue.empty()
        assert queue.pop() == 42
    
    def test_consumer(self):
        """Test that the consumer pulls values from the queue."""
        queue = ThreadSafeQueue[int](5)
        running = threading.Event()
        running.set()
        
        # Add items to the queue
        test_values = [1, 2, 3]
        for val in test_values:
            queue.push(val)
        
        # Create a consumer and run it in a thread
        consumer = Consumer(queue, running, 1, delay=0.01)
        consumer_thread = threading.Thread(target=consumer)
        
        # Run the consumer
        consumer_thread.start()
        
        # Wait a bit to let the consumer process all items
        time.sleep(0.1)
        
        # Signal the consumer to stop after emptying the queue
        running.clear()
        
        # Signal that no more items will be produced
        queue.set_no_more_producers()
        
        # Wait for the consumer to finish with a timeout
        consumer_thread.join(timeout=1.0)
        
        # Check if the thread is still alive
        if consumer_thread.is_alive():
            # This shouldn't happen, but if it does, we'll help clean up
            pytest.fail("Consumer thread did not terminate properly")
            
        # Verify all items were consumed
        assert queue.empty()


if __name__ == "__main__":
    pytest.main(["-v", __file__])