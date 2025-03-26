#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Custom configuration example for the producer-consumer pattern.

This example demonstrates how to customize the producer-consumer parameters
and create a custom workflow with different production/consumption rates.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from icecream import ic

# When running as a module, use direct import
try:
    from producer_consumer.producer_consumer import run_producer_consumer_demo
except ImportError:
    # When running from example directory, use this import
    from src.producer_consumer.producer_consumer import run_producer_consumer_demo


def run_custom_example() -> None:
    """
    Run a customized producer-consumer example with specific parameters.
    """
    ic.configureOutput(prefix="[Custom Example] ")
    
    # Custom parameters
    queue_capacity = 5  # Smaller queue to demonstrate backpressure
    num_producers = 3   # More producers than consumers
    num_consumers = 2
    run_time = 5        # Adjusted run time for quicker demo
    
    # Run with custom parameters
    ic("Starting custom producer-consumer example")
    ic(f"Queue capacity: {queue_capacity}")
    ic(f"Number of producers: {num_producers}")
    ic(f"Number of consumers: {num_consumers}")
    ic(f"Run time: {run_time} seconds")
    
    run_producer_consumer_demo(
        queue_capacity=queue_capacity,
        num_producers=num_producers,
        num_consumers=num_consumers,
        run_time=run_time
    )
    
    ic("Custom example completed")


if __name__ == "__main__":
    run_custom_example()