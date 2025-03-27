#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Example demonstrating basic usage of the ThreadPool class.
"""

import sys
import time
from pathlib import Path

# Add the project directory to the path so we can import the package
project_dir = Path(__file__).resolve().parent.parent
src_dir = project_dir / "src"
sys.path.insert(0, str(project_dir))
sys.path.insert(0, str(src_dir))

from thread_pool.thread_pool import LogLevel, Logger, ThreadPool


def main() -> None:
    """Demonstrate basic usage of the ThreadPool."""
    # Get the logger instance
    logger = Logger.get_instance()
    logger.log(LogLevel.INFO, "Starting ThreadPool example")
    
    # Create a thread pool with 4 threads
    pool = ThreadPool(4, logger)
    
    # Example 1: Execute a simple lambda
    logger.log(LogLevel.INFO, "Example 1: Execute a simple lambda")
    future1 = pool.enqueue(lambda x: x * x, 42)
    result1 = future1.result()
    logger.log(LogLevel.INFO, f"Result of 42 * 42 = {result1}")
    
    # Example 2: Execute a function
    def multiply(x: float, y: float) -> float:
        return x * y
    
    logger.log(LogLevel.INFO, "Example 2: Execute a function")
    future2 = pool.enqueue(multiply, 3.14, 2.0)
    result2 = future2.result()
    logger.log(LogLevel.INFO, f"Result of 3.14 * 2.0 = {result2}")
    
    # Example 3: Process a list of items in parallel
    logger.log(LogLevel.INFO, "Example 3: Process a list of items in parallel")
    items = list(range(1, 11))
    futures = [pool.enqueue(lambda x: x * x, item) for item in items]
    
    # Collect results
    results = [future.result() for future in futures]
    logger.log(LogLevel.INFO, f"Squared numbers: {results}")
    
    # Example 4: Handle exceptions
    logger.log(LogLevel.INFO, "Example 4: Handle exceptions")
    future_ex = pool.enqueue(lambda: 1 / 0)
    
    try:
        result_ex = future_ex.result()
    except ZeroDivisionError:
        logger.log(LogLevel.ERROR, "Caught division by zero error, as expected")
    
    # Example 5: Parallel processing with real work
    logger.log(LogLevel.INFO, "Example 5: Parallel processing with real work")
    
    def process_item(item: int) -> int:
        """Simulate processing an item with some delay."""
        logger.log(LogLevel.INFO, f"Processing item {item}")
        time.sleep(1)  # Simulate work
        return item * 10
    
    # Process 8 items in parallel
    batch = list(range(8))
    
    start_time = time.time()
    futures = [pool.enqueue(process_item, item) for item in batch]
    results = [future.result() for future in futures]
    end_time = time.time()
    
    logger.log(LogLevel.INFO, f"Processed {len(batch)} items in {end_time - start_time:.2f} seconds")
    logger.log(LogLevel.INFO, f"Results: {results}")
    
    # Clean shutdown
    pool.shutdown()
    logger.log(LogLevel.INFO, "ThreadPool example completed")


if __name__ == "__main__":
    main()