#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the visitor pattern example.

This script provides a convenient way to run the visitor pattern example
without having to use the module import syntax.
"""

import sys
from pathlib import Path

# Add the src directory to the path so we can import the visitor_pattern package
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

try:
    from visitor_pattern.vistor import main

    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Error importing visitor_pattern package: {e}")
    print("Make sure you have installed the package or are running from the correct directory.")
    sys.exit(1)
