#!/usr/bin/env python3
"""Example using the modern barrier implementation."""

import sys
from pathlib import Path

# Add the src directory to the Python path
script_dir = Path(__file__).parent.parent
sys.path.insert(0, str(script_dir / "src"))

from barrier_example.examples import IceCreamLogger


def main() -> None:
    """Run a demonstration of the modern barrier implementation."""
    NUM_THREADS = 4
    logger = IceCreamLogger()

    # Import and run the demonstration
    from barrier_example.examples import ModernBarrierExample

    ModernBarrierExample.demonstrate(NUM_THREADS, logger)


if __name__ == "__main__":
    main()
