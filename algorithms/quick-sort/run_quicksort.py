#!/usr/bin/env python3
"""
QuickSort launcher script.

This script provides direct execution of the QuickSort algorithm without
requiring module imports. It ensures the package is in the Python path
and calls the main function.
"""

import sys
from pathlib import Path


def main() -> None:
    """
    Run the QuickSort demonstration.
    
    Adds the project directory to the Python path and calls the main function
    from the quicksort package.
    """
    # Add the src directory to Python path
    project_root = Path(__file__).parent.absolute()
    sys.path.insert(0, str(project_root))

    try:
        from src.quicksort.quick_sort import main as quicksort_main
        quicksort_main()
    except ImportError as e:
        print(f"Error importing quicksort package: {e}")
        print("Make sure you have installed the package or are running from the correct directory.")
        sys.exit(1)


if __name__ == "__main__":
    main()
