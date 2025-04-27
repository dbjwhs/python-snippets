#!/usr/bin/env python3
"""
Launcher script for the abstract factory pattern demonstration.

This script adds the appropriate directories to the Python path and launches
the abstract factory demo.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

try:
    from src.abstract_factory.abstract_factory import main
    main()
except ImportError as e:
    print(f"Error importing abstract factory module: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error running abstract factory demo: {e}")
    sys.exit(1)