"""
Example demonstrating the Adapter pattern with file systems.

This example shows how to use adapters to work with different file systems
through a unified interface.
"""

from adapter_pattern.adapter import APFSAdapter, FAT32Adapter, FileOperationsManager, ic


def demonstrate_cross_platform_file_operations() -> None:
    """Show how to use adapters for cross-platform file operations."""
    ic("Starting cross-platform file operations demo")

    # Example 1: Working with APFS adapter
    apfs_manager = FileOperationsManager(APFSAdapter())

    ic("APFS Example")
    ic("-" * 40)

    # Demonstrate APFS operations
    apfs_manager.file_system.create_directory("/Users/demo/Documents/project")
    apfs_manager.file_system.copy_file(
        "/Users/demo/source.txt",
        "/Users/demo/Documents/project/dest.txt"
    )

    files = apfs_manager.file_system.list_files("/Users/demo/Documents/project")
    ic("Files in APFS directory:", files)

    ic(f"Supports symlinks: {apfs_manager.file_system.supports_symlinks()}")
    ic(f"Supports permissions: {apfs_manager.file_system.supports_permissions()}")

    # Example 2: Working with FAT32 adapter
    fat32_manager = FileOperationsManager(FAT32Adapter())

    ic("\nFAT32 Example")
    ic("-" * 40)

    # Demonstrate FAT32 operations
    fat32_manager.file_system.create_directory("D:\\PROJECT")
    fat32_manager.file_system.copy_file(
        "D:\\SOURCE.TXT",
        "D:\\PROJECT\\DEST.TXT"
    )

    files = fat32_manager.file_system.list_files("D:\\PROJECT")
    ic("Files in FAT32 directory:", files)

    ic(f"Supports symlinks: {fat32_manager.file_system.supports_symlinks()}")
    ic(f"Supports permissions: {fat32_manager.file_system.supports_permissions()}")

    # Example 3: Cross-system file operations
    ic("\nCross-System Operation Example")
    ic("-" * 40)

    # Using FAT32 adapter to copy from APFS (simulated)
    source_file = "/Users/demo/Documents/project*.txt"
    dest_file = "D:\\PROJECT\\BACKUP"

    fat32_manager.perform_cross_system_copy(source_file, dest_file)

    # Example 4: Handling problematic file names
    ic("\nHandling Problematic Filenames")
    ic("-" * 40)

    # APFS handling of problematic names
    apfs_adapter = APFSAdapter()
    success = apfs_adapter.create_directory(".hidden/directory:with/special\0chars")
    ic(f"APFS handling of special characters: {'Success' if success else 'Failed'}")

    # FAT32 handling of problematic names
    fat32_adapter = FAT32Adapter()
    success = fat32_adapter.create_directory("Long folder name with <invalid> chars*?.txt")
    ic(f"FAT32 handling of special characters: {'Success' if success else 'Failed'}")

    ic("Cross-platform file operations demo completed")


if __name__ == "__main__":
    demonstrate_cross_platform_file_operations()
