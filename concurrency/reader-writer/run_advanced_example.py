#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the advanced example of the reader_writer package.

This script adds the necessary directories to the Python path and
launches the advanced example.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
root_dir = Path(__file__).parent.absolute()
src_dir = root_dir / "src"
sys.path.insert(0, str(src_dir))

# Import and run the advanced example
if __name__ == "__main__":
    try:
        from examples.advanced_usage import advanced_example
        advanced_example()
    except ImportError as e:
        print(f"Error importing the example: {e}")
        print("Make sure you have installed the package with 'uv pip install -e .'")
        sys.exit(1)
    except Exception as e:
        print(f"Error running the example: {e}")
        sys.exit(1)