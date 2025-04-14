#!/usr/bin/env python3
"""
Example runner script for QuickSort.

This script runs the examples in the examples directory, making sure
the package is in the Python path.
"""

import sys
from pathlib import Path


def main() -> None:
    """
    Run the QuickSort examples.
    
    Adds the project directory to the Python path and runs the basic_usage example.
    """
    # Add the project directory to Python path
    project_root = Path(__file__).parent.absolute()
    sys.path.insert(0, str(project_root))

    try:
        from examples.basic_usage import main as example_main
        example_main()
    except ImportError as e:
        print(f"Error importing example: {e}")
        print("Make sure you have installed the package or are running from the correct directory.")
        sys.exit(1)


if __name__ == "__main__":
    main()
