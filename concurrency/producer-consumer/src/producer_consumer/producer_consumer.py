# MIT License
# Copyright (c) 2025 dbjwhs

"""
Thread-safe Producer-Consumer implementation in Python.

This module provides classes for implementing the Producer-Consumer pattern
with a thread-safe queue, producer, and consumer.
"""

import queue
import random
import threading
import time
from dataclasses import dataclass
from threading import Condition, Lock
from typing import Generic, TypeVar

from icecream import ic

# Type variable for the queue's content type
T = TypeVar('T')


class ThreadSafeQueue(Generic[T]):
    """
    Thread-safe queue implementation with bounded capacity.

    Provides synchronized access for multiple producers and consumers
    with condition variables for coordination.
    """

    def __init__(self, max_size: int) -> None:
        """
        Initialize a new thread-safe queue with specified capacity.

        Args:
            max_size: Maximum number of items the queue can hold
        """
        self._queue: queue.Queue[T] = queue.Queue(maxsize=max_size)
        self._mutex = Lock()
        self._not_empty = Condition(self._mutex)
        self._not_full = Condition(self._mutex)
        self._capacity = max_size
        self._no_more_producers = False  # Flag to signal when all producers have stopped

    def push(self, value: T) -> None:
        """
        Add an item to the queue, blocking if the queue is full.

        Args:
            value: The item to be added to the queue
        """
        with self._mutex:
            while self._queue.qsize() >= self._capacity:
                self._not_full.wait()
            self._queue.put(value)
            self._not_empty.notify()

    def pop(self, timeout: float | None = 0.5) -> T:
        """
        Remove and return an item from the queue, blocking if queue is empty.

        Args:
            timeout: Maximum time to wait for an item. None means wait indefinitely.
                    Default is 0.5 seconds.

        Returns:
            The next item from the queue
        
        Raises:
            RuntimeError: If the queue is empty and no more producers are running
        """
        with self._mutex:
            while self._queue.empty():
                # If no more items will be produced and the queue is empty, we're done
                if self._no_more_producers:
                    error_msg = "Queue is empty and no more producers are running"
                    raise RuntimeError(error_msg)
                
                # Wait with a timeout to prevent indefinite blocking
                # If timeout is None, wait indefinitely
                if timeout is None:
                    self._not_empty.wait()
                    continue
                    
                if not self._not_empty.wait(timeout=timeout):
                    # Timeout occurred, check again if we should exit
                    if self._queue.empty() and self._no_more_producers:
                        error_msg = "Queue is empty and no more producers are running"
                        raise RuntimeError(error_msg)
                    # Otherwise continue waiting
                    continue
            
            value = self._queue.get()
            self._not_full.notify()
            return value
            
    def set_no_more_producers(self) -> None:
        """
        Signal that no more items will be produced.
        This helps prevent consumer threads from waiting indefinitely.
        """
        with self._mutex:
            self._no_more_producers = True
            # Wake up any waiting consumer threads
            self._not_empty.notify_all()

    def empty(self) -> bool:
        """
        Check if the queue is empty.

        Returns:
            True if queue is empty, False otherwise
        """
        with self._mutex:
            return self._queue.empty()

    def size(self) -> int:
        """
        Get the current number of items in the queue.

        Returns:
            Current queue size
        """
        with self._mutex:
            return self._queue.qsize()


@dataclass
class Producer:
    """
    Producer class that generates random values and pushes them to a queue.

    Uses thread-safe operations to coordinate with consumers.
    """

    queue: ThreadSafeQueue[int]
    running: threading.Event
    producer_id: int
    delay: float = 0.5  # seconds between productions

    def __call__(self) -> None:
        """Produce items until signaled to stop."""
        while self.running.is_set():
            value = random.randint(1, 100)
            self.queue.push(value)
            ic(f"Producer {self.producer_id} produced: {value}")
            time.sleep(self.delay)


@dataclass
class Consumer:
    """
    Consumer class that takes values from a queue and processes them.

    Uses thread-safe operations to coordinate with producers.
    """

    queue: ThreadSafeQueue[int]
    running: threading.Event
    consumer_id: int
    delay: float = 1.0  # seconds between consumptions

    def __call__(self) -> None:
        """Consume items until signaled to stop and queue is empty."""
        try:
            # Continue running if either:
            # 1. We're explicitly told to run (self.running.is_set())
            # 2. The queue isn't empty, so we have work to do
            while self.running.is_set() or not self.queue.empty():
                try:
                    # Check more frequently if we should stop
                    if not self.running.is_set() and self.queue.empty():
                        break
                        
                    # Use a shorter timeout if we're in shutdown mode
                    timeout = 0.1 if not self.running.is_set() else None
                    
                    # Try to pop an item with the appropriate timeout
                    value = self.queue.pop(timeout=timeout)
                    ic(f"Consumer {self.consumer_id} consumed: {value}")
                    
                    # Sleep for a shorter time if we're in shutdown mode
                    sleep_time = min(0.1, self.delay) if not self.running.is_set() else self.delay
                    time.sleep(sleep_time)
                    
                except RuntimeError:
                    # Queue is empty and no more producers are running
                    ic(f"Consumer {self.consumer_id} stopping: no more items to process")
                    break
        except Exception as e:
            ic(f"Consumer {self.consumer_id} encountered an error: {e}")


def run_producer_consumer_demo(
    queue_capacity: int = 10,
    num_producers: int = 2,
    num_consumers: int = 3,
    run_time: int = 10  # seconds
) -> None:
    """
    Run a demonstration of the producer-consumer pattern.

    Args:
        queue_capacity: Size of the shared queue
        num_producers: Number of producer threads to create
        num_consumers: Number of consumer threads to create
        run_time: How long to run the simulation in seconds
    """
    # Initialize the queue and running event
    thread_queue: ThreadSafeQueue[int] = ThreadSafeQueue(queue_capacity)
    running = threading.Event()
    running.set()  # Start in running state

    # Create and start producer threads
    producer_threads: list[threading.Thread] = []
    for ndx in range(num_producers):
        producer = Producer(thread_queue, running, ndx + 1)
        thread = threading.Thread(target=producer, name=f"Producer-{ndx+1}")
        thread.start()
        producer_threads.append(thread)

    # Create and start consumer threads
    consumer_threads: list[threading.Thread] = []
    for ndx in range(num_consumers):
        consumer = Consumer(thread_queue, running, ndx + 1)
        thread = threading.Thread(target=consumer, name=f"Consumer-{ndx+1}")
        thread.start()
        consumer_threads.append(thread)

    # Run for specified time
    time.sleep(run_time)
    
    # Signal threads to stop
    running.clear()
    
    # Wait for all producer threads to finish
    for thread in producer_threads:
        thread.join()
        
    # Signal that no more items will be produced
    thread_queue.set_no_more_producers()
    ic("All producers have finished")
    
    # Wait for all consumer threads to finish
    remaining_threads = []
    for thread in consumer_threads:
        # First attempt to join with timeout
        thread.join(timeout=1.0)
        
        # Check if thread is still running
        if thread.is_alive():
            remaining_threads.append(thread)
    
    if remaining_threads:
        ic(f"{len(remaining_threads)} consumer threads still running, waiting again...")
        
        # For any remaining threads, try once more
        for thread in remaining_threads:
            # Ensure we have the latest queue state
            thread_queue.set_no_more_producers()
            thread.join(timeout=1.0)
            
            if thread.is_alive():
                ic(f"Warning: Consumer thread {thread.name} did not finish properly")
    
    ic("All threads have finished")


if __name__ == "__main__":
    ic.configureOutput(prefix="[Producer-Consumer] ")
    run_producer_consumer_demo()