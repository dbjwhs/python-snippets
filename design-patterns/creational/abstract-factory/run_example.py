#!/usr/bin/env python3
"""
Launcher script for the theme switcher example.

This script adds the appropriate directories to the Python path and launches
the theme switcher example application.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

try:
    from examples.theme_switcher import main
    main()
except ImportError as e:
    print(f"Error importing theme switcher module: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error running theme switcher example: {e}")
    sys.exit(1)