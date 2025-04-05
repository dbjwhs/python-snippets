#!/usr/bin/env python3
"""
Launcher script for the advanced slicing example.

This script adds necessary directories to the Python path
and runs the advanced example demonstrating more complex
object copying and serialization issues.
"""

import os
import sys
from pathlib import Path


# Add the src directory to the Python path
current_dir = Path(__file__).parent
examples_dir = current_dir / "slicing" / "examples"
src_dir = current_dir / "slicing" / "src"
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(examples_dir))

try:
    from advanced_example import demonstrate_advanced_issues
    
    if __name__ == "__main__":
        demonstrate_advanced_issues()
except ImportError as e:
    print(f"Error importing the advanced example: {e}")
    print("Make sure you have installed the package or are running from the correct directory.")
    sys.exit(1)