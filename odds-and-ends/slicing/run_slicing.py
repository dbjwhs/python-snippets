#!/usr/bin/env python3
"""
Launcher script for the slicing example.

This script adds necessary directories to the Python path
and runs the main slicing demonstration.
"""

import os
import sys
from pathlib import Path


# Add the src directory to the Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "slicing" / "src"
sys.path.insert(0, str(src_dir))

try:
    from slicing import run_demo
    
    if __name__ == "__main__":
        run_demo()
except ImportError as e:
    print(f"Error importing the slicing module: {e}")
    print("Make sure you have installed the package or are running from the correct directory.")
    sys.exit(1)