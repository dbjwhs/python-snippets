#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""Launcher script for the negative space demonstration.

This script allows direct execution without module imports.
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from negative_space.negative_space import main

if __name__ == "__main__":
    main()