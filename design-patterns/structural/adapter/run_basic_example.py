#!/usr/bin/env python3
"""
Basic Adapter Example Launcher

This script runs the basic power adapter pattern demonstration.
"""

import os
import sys

# Get the directory this script is in
script_dir = os.path.dirname(os.path.abspath(__file__))

# Run the adapter module from the correct dir
os.chdir(script_dir)

# Make sure adapter_pattern is in the Python path
sys.path.insert(0, script_dir)

# Run as a script directly
os.system('cd "{}" && python3 adapter_pattern/src/adapter_pattern/examples/basic_adapter_standalone.py'.format(script_dir))
