#!/usr/bin/env python3
"""
Standalone executable for the adapter pattern demonstration.

This file can be run directly to demonstrate the adapter pattern.
"""

import sys
import os

# Add parent directory to the path to make imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, parent_dir)

from src.adapter_pattern.adapter import main as file_system_main
from src.adapter_pattern.examples.file_system_example import demonstrate_cross_platform_file_operations
from src.adapter_pattern.examples.basic_adapter_example import demonstrate_power_adapters

from icecream import ic


def main() -> None:
    """Run the adapter pattern examples."""
    ic("Adapter Pattern Demonstrations")
    ic("=" * 50)
    
    # Option 1: Run the file system adapter tests
    ic("\nRunning File System Adapter Tests:\n")
    file_system_main()
    
    # Option 2: Demonstrate cross-platform file operations
    ic("\nDemonstrating Cross-Platform File Operations:\n")
    demonstrate_cross_platform_file_operations()
    
    # Option 3: Demonstrate basic power adapter example
    ic("\nDemonstrating Basic Power Adapter Example:\n")
    demonstrate_power_adapters()


if __name__ == "__main__":
    main()