#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the HighResolutionTimer basic usage example.

This script adds the necessary directories to the Python path
and imports and calls the main function directly.
"""

import os
import sys

# Add the src directory to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, "src")
sys.path.insert(0, src_dir)
examples_dir = os.path.join(script_dir, "examples")
sys.path.insert(0, script_dir)

from examples.basic_usage import main  # noqa: E402

if __name__ == "__main__":
    main()
