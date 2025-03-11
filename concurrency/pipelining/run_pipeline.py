#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the basic pipeline example.

This script provides direct execution of the pipeline example without 
requiring module imports.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import and run the main function
from src.pipeline.__main__ import main

if __name__ == "__main__":
    main()