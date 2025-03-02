#!/usr/bin/env python
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the Interpreter pattern implementation.

This script provides an easy way to run the interpreter pattern
without having to use the module syntax (python -m interpreter_pattern).
"""

import sys
import os

# Add the src directory to the Python path to enable importing the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# Import the main function from the package
from interpreter_pattern.__main__ import main


if __name__ == "__main__":
    # Call the main function directly
    main()