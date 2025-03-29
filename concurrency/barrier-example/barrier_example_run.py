#!/usr/bin/env python3
"""Launcher script for the barrier example.

This script adds the src directory to the Python path and runs the main function.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
src_dir = script_dir / "src"
sys.path.insert(0, str(src_dir))

# Import and run the main function
try:
    from barrier_example.__main__ import main

    main()
except ImportError as e:
    print(f"Error importing barrier_example: {e}")
    print("Make sure you have installed all dependencies.")
    sys.exit(1)
