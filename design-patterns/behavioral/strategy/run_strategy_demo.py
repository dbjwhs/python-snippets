#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the Strategy Pattern demo.

This script will run the main demo showing different payment strategies.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

try:
    from strategy_pattern.__main__ import main
    
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Error importing strategy_pattern package: {e}")
    print("Make sure you have installed the package or are running from the correct directory.")
    sys.exit(1)