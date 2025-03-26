#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the custom producer-consumer example.

This script runs the custom producer-consumer configuration example.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from examples.custom_config_example import run_custom_example
from icecream import ic

if __name__ == "__main__":
    ic("Launching custom producer-consumer example")
    run_custom_example()