#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the Producer-Consumer demonstration.

This script allows running the producer-consumer demo without module imports.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from icecream import ic

# When running as a module, use direct import
try:
    from producer_consumer.producer_consumer import run_producer_consumer_demo
except ImportError:
    # When running from root directory, use this import
    from src.producer_consumer.producer_consumer import run_producer_consumer_demo

if __name__ == "__main__":
    ic.configureOutput(prefix="[Producer-Consumer] ")
    ic("Starting producer-consumer demonstration with default settings")
    # Default runtime is 10 seconds, but you can adjust parameters as needed
    run_producer_consumer_demo(
        queue_capacity=100,
        num_producers=20,
        num_consumers=30,
        run_time=30
    )