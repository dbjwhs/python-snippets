#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Example demonstrating advanced usage of the ThreadPool class.
"""

import sys
import time
from concurrent.futures import as_completed
from pathlib import Path

# Add the project directory to the path so we can import the package
project_dir = Path(__file__).resolve().parent.parent
src_dir = project_dir / "src"
sys.path.insert(0, str(project_dir))
sys.path.insert(0, str(src_dir))

from thread_pool.thread_pool import LogLevel, Logger, ThreadPool


def cpu_intensive_task(n: int) -> tuple[int, int]:
    """A CPU-intensive task that computes the sum of squares up to n."""
    result = sum(i * i for i in range(n))
    return n, result


def io_intensive_task(delay: float, identifier: str) -> tuple[str, float]:
    """An I/O-intensive task that simulates network or disk I/O with a delay."""
    time.sleep(delay)  # Simulate I/O operation
    return identifier, delay


def main() -> None:
    """Demonstrate advanced usage of the ThreadPool."""
    # Get the logger instance
    logger = Logger.get_instance()
    logger.log(LogLevel.INFO, "Starting advanced ThreadPool example")
    
    # Create a thread pool with the number of CPU cores
    import threading
    num_threads = max(4, threading.cpu_count())
    logger.log(LogLevel.INFO, f"Creating thread pool with {num_threads} threads")
    pool = ThreadPool(num_threads, logger)
    
    # Example 1: Process tasks as they complete
    logger.log(LogLevel.INFO, "Example 1: Process tasks as they complete")
    
    # Submit 10 CPU-intensive tasks
    cpu_futures = [pool.enqueue(cpu_intensive_task, i * 1000) for i in range(10)]
    
    # Process results as they complete
    for future in as_completed(cpu_futures):
        n, result = future.result()
        logger.log(LogLevel.INFO, f"Task for n={n} completed with result: {result}")
    
    # Example 2: Mix of CPU and I/O tasks
    logger.log(LogLevel.INFO, "Example 2: Mix of CPU and I/O tasks")
    
    # Create a mix of CPU and I/O tasks
    mixed_futures = []
    for i in range(5):
        # Add a CPU-intensive task
        mixed_futures.append(pool.enqueue(cpu_intensive_task, i * 500))
        # Add an I/O-intensive task
        mixed_futures.append(pool.enqueue(
            io_intensive_task, 
            delay=0.5 + (i * 0.1),
            identifier=f"IO-Task-{i}"
        ))
    
    # Collect results
    cpu_results: dict[int, int] = {}
    io_results: dict[str, float] = {}
    
    for future in as_completed(mixed_futures):
        result = future.result()
        
        # Determine the type of result
        if isinstance(result[0], int):
            # CPU task result
            n, value = result
            cpu_results[n] = value
        else:
            # I/O task result
            identifier, delay = result
            io_results[identifier] = delay
    
    logger.log(LogLevel.INFO, f"CPU task results: {cpu_results}")
    logger.log(LogLevel.INFO, f"I/O task results: {io_results}")
    
    # Example 3: Error handling and task cancellation
    logger.log(LogLevel.INFO, "Example 3: Error handling and task cancellation")
    
    def faulty_task(succeed: bool) -> bool:
        """A task that may succeed or fail based on the input."""
        time.sleep(0.5)  # Simulate work
        if not succeed:
            raise ValueError("Task was set to fail")
        return succeed
    
    # Submit a mix of succeeding and failing tasks
    error_futures = [
        pool.enqueue(faulty_task, i % 2 == 0) for i in range(10)
    ]
    
    # Cancel some tasks (note: they may already be running)
    for i, future in enumerate(error_futures):
        if i % 3 == 0:
            logger.log(LogLevel.INFO, f"Attempting to cancel task {i}")
            future.cancel()
    
    # Process results with proper error handling
    for i, future in enumerate(error_futures):
        try:
            if future.cancelled():
                logger.log(LogLevel.INFO, f"Task {i} was cancelled")
            else:
                result = future.result()
                logger.log(LogLevel.INFO, f"Task {i} succeeded with result: {result}")
        except ValueError as e:
            logger.log(LogLevel.ERROR, f"Task {i} failed with error: {e}")
    
    # Example 4: Batch processing with dependencies
    logger.log(LogLevel.INFO, "Example 4: Batch processing with dependencies")
    
    # First batch: Generate data
    data_futures = [pool.enqueue(lambda i=i: [i * j for j in range(10)], i) for i in range(5)]
    
    # Wait for all data generation to complete
    data_batches = [future.result() for future in data_futures]
    logger.log(LogLevel.INFO, f"Generated {len(data_batches)} data batches")
    
    # Second batch: Process the generated data
    result_futures = []
    for batch in data_batches:
        result_futures.append(pool.enqueue(lambda b: sum(b), batch))
    
    # Collect and display results
    batch_results = [future.result() for future in result_futures]
    logger.log(LogLevel.INFO, f"Batch processing results: {batch_results}")
    
    # Clean shutdown
    pool.shutdown()
    logger.log(LogLevel.INFO, "Advanced ThreadPool example completed")


if __name__ == "__main__":
    main()