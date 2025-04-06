"""
Main entry point for the adapter pattern package.

This module demonstrates both examples of the adapter pattern.
"""

from icecream import ic

from adapter_pattern.adapter import main as file_system_main
from adapter_pattern.examples.basic_adapter_example import demonstrate_power_adapters
from adapter_pattern.examples.file_system_example import demonstrate_cross_platform_file_operations


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
