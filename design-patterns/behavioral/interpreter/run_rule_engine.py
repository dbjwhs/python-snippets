#!/usr/bin/env python
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the Rule Engine example.

This script provides an easy way to run the rule engine example
without having to worry about Python path issues.
"""

import sys
import os

# Add the src directory to the Python path to enable importing the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# Import the main function from the example
from examples.rule_engine_example import main


if __name__ == "__main__":
    # Call the main function directly
    main()