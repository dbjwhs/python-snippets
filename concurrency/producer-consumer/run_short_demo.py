#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Short demonstration of the Producer-Consumer pattern.

This script runs a brief demo that will complete quickly.
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
    ic.configureOutput(prefix="[Demo] ")
    ic("Starting short producer-consumer demonstration (2 second runtime)")
    # Run with just 2 second runtime for quick testing
    run_producer_consumer_demo(
        queue_capacity=5,
        num_producers=1,
        num_consumers=1,
        run_time=2
    )