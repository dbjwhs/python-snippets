#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the Proxy pattern demo.

This script runs the main proxy pattern demonstration, showing
protection proxy with authentication and logging.
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from proxy_pattern import Logger, LogLevel, main
    
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Make sure you've installed the package with 'uv pip install -e .'")
    sys.exit(1)