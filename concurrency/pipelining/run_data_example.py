#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the data processing pipeline example.

This script provides direct execution of the data processing example without 
requiring module imports.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import and run the main function
from examples.data_processing_example import main

if __name__ == "__main__":
    main()