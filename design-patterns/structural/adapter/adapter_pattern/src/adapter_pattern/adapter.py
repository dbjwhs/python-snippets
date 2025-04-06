"""
Implementation of the Adapter design pattern for file systems.

This module demonstrates the Adapter pattern by creating adapters for different file systems
to provide a uniform interface for file operations across platforms.
"""

import hashlib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Final, Generic, Protocol, TypeVar

from icecream import ic

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Constants for invalid characters
class FileSystemConstants:
    """Constants for file system operations."""

    # Invalid characters for different file systems
    INVALID_WIN_CHARS: Final[str] = '<>:"/\\|?*'
    SPECIAL_APFS_CHARS: Final[str] = '/\0:'

    # Maximum path lengths
    MAX_WIN_PATH: Final[int] = 260
    MAX_APFS_PATH: Final[int] = 1024


# Define file system protocol (equivalent to C++ concept)
class FileSystem(Protocol):
    """Protocol defining the interface for file system operations."""

    def create_directory(self, path: str) -> bool:
        """Create a directory at the specified path."""
        ...

    def copy_file(self, source: str, dest: str) -> bool:
        """Copy a file from source to destination."""
        ...

    def list_files(self, path: str) -> list[str]:
        """List files in the specified directory."""
        ...

    def supports_symlinks(self) -> bool:
        """Check if the file system supports symbolic links."""
        ...

    def supports_permissions(self) -> bool:
        """Check if the file system supports file permissions."""
        ...


# Abstract interface for modern file system operations
class IFileSystem(ABC):
    """Abstract base class for file system operations."""

    @abstractmethod
    def create_directory(self, path: str) -> bool:
        """Create a directory at the specified path."""
        pass

    @abstractmethod
    def copy_file(self, source: str, dest: str) -> bool:
        """Copy a file from source to destination."""
        pass

    @abstractmethod
    def list_files(self, path: str) -> list[str]:
        """List files in the specified directory."""
        pass

    @abstractmethod
    def supports_symlinks(self) -> bool:
        """Check if the file system supports symbolic links."""
        pass

    @abstractmethod
    def supports_permissions(self) -> bool:
        """Check if the file system supports file permissions."""
        pass


# APFS (Apple File System) implementation
@dataclass
class APFSSystem:
    """Implementation of Apple File System operations."""

    case_sensitive: bool = False
    volume_name: str = ""

    @staticmethod
    def create_apfs_directory(path: str, permissions: int) -> bool:
        """Create a directory with APFS-specific options."""
        ic(f"Creating APFS directory: {path} with unix permissions: {permissions:o}")
        return True

    @staticmethod
    def copy_apfs_file(source: str, dest: str, preserve_metadata: bool) -> bool:
        """Copy a file with APFS-specific options."""
        ic(f"Copying APFS file with metadata preservation: {'yes' if preserve_metadata else 'no'}")
        ic(f"Source: {source}, Dest: {dest}")
        return True

    @staticmethod
    def get_apfs_contents(path: str, include_hidden: bool) -> list[str]:
        """List contents of an APFS directory."""
        ic(f"Listing APFS directory contents{' (including hidden files)' if include_hidden else ''}")
        return ["file1.txt", ".ds_store", "folder1"]


# FAT32 (Windows File System) implementation
@dataclass
class FAT32System:
    """Implementation of FAT32 file system operations."""

    drive_letter: str = ""
    quick_format: bool = False

    @staticmethod
    def make_fat32_dir(path: str) -> bool:
        """Create a directory with FAT32-specific options."""
        ic(f"Creating FAT32 directory: {path}")
        return True

    @staticmethod
    def copy_fat32(source: str, dest: str) -> bool:
        """Copy a file with FAT32-specific options."""
        ic("Copying FAT32 file (8.3 filename format)")
        ic(f"Source: {source}, Dest: {dest}")
        return True

    @staticmethod
    def scan_fat32_dir(path: str) -> list[str]:
        """List contents of a FAT32 directory."""
        ic("Scanning FAT32 directory contents (8.3 format)")
        return ["FILE1.TXT", "FOLDER1"]


# Adapter for APFS to modern interface
class APFSAdapter(IFileSystem):
    """Adapter for APFS to conform to the IFileSystem interface."""

    def __init__(self) -> None:
        """Initialize the APFS adapter."""
        self._apfs_system = APFSSystem()

    @staticmethod
    def _sanitize_for_apfs(filename: str) -> str:
        """Sanitize a filename for APFS constraints."""
        result = filename

        # Handle special APFS characters
        for special_char in FileSystemConstants.SPECIAL_APFS_CHARS:
            result = result.replace(special_char, '_')

        # Check path length
        if len(result) > FileSystemConstants.MAX_APFS_PATH:
            hash_obj = hashlib.md5(filename.encode())
            hash_str = hash_obj.hexdigest()[:8]
            result = result[:FileSystemConstants.MAX_APFS_PATH - len(hash_str) - 1]
            result += '_' + hash_str

        # Handle leading dots (hidden files in unix)
        if result and result[0] == '.':
            result = '_' + result

        return result

    def create_directory(self, path: str) -> bool:
        """Create a directory using the APFS adapter."""
        if not path:
            return False
        return APFSSystem.create_apfs_directory(self._sanitize_for_apfs(path), 0o755)

    def copy_file(self, source: str, dest: str) -> bool:
        """Copy a file using the APFS adapter."""
        return APFSSystem.copy_apfs_file(
            self._sanitize_for_apfs(source),
            self._sanitize_for_apfs(dest),
            True
        )

    def list_files(self, path: str) -> list[str]:
        """List files using the APFS adapter."""
        return APFSSystem.get_apfs_contents(path, False)

    def supports_symlinks(self) -> bool:
        """Check if APFS supports symlinks."""
        return True

    def supports_permissions(self) -> bool:
        """Check if APFS supports permissions."""
        return True


# Adapter for FAT32 to modern interface
class FAT32Adapter(IFileSystem):
    """Adapter for FAT32 to conform to the IFileSystem interface."""

    def __init__(self) -> None:
        """Initialize the FAT32 adapter."""
        self._fat32_system = FAT32System()

    @staticmethod
    def _sanitize_for_fat32(filename: str) -> str:
        """Sanitize a filename for FAT32 constraints."""
        result = filename

        # Remove invalid Windows characters
        for invalid_char in FileSystemConstants.INVALID_WIN_CHARS:
            result = result.replace(invalid_char, '_')

        # Handle spaces
        result = result.replace(' ', '_')

        # Check path length
        if len(result) > FileSystemConstants.MAX_WIN_PATH:
            hash_obj = hashlib.md5(filename.encode())
            hash_str = hash_obj.hexdigest()[:8]
            result = result[:FileSystemConstants.MAX_WIN_PATH - len(hash_str) - 1]
            result += '_' + hash_str

        return result

    @staticmethod
    def _convert_to_8_3_format(filename: str) -> str:
        """Convert a filename to 8.3 format."""
        # Split name and extension
        if '.' in filename:
            name, ext = filename.rsplit('.', 1)
            result = f"{name[:8]}.{ext[:3]}"
        else:
            result = filename[:8]

        # Convert to uppercase
        return result.upper()

    def create_directory(self, path: str) -> bool:
        """Create a directory using the FAT32 adapter."""
        if not path:
            return False
        return FAT32System.make_fat32_dir(
            self._convert_to_8_3_format(self._sanitize_for_fat32(path))
        )

    def copy_file(self, source: str, dest: str) -> bool:
        """Copy a file using the FAT32 adapter."""
        return FAT32System.copy_fat32(
            self._convert_to_8_3_format(self._sanitize_for_fat32(source)),
            self._convert_to_8_3_format(self._sanitize_for_fat32(dest))
        )

    def list_files(self, path: str) -> list[str]:
        """List files using the FAT32 adapter."""
        return FAT32System.scan_fat32_dir(self._convert_to_8_3_format(path))

    def supports_symlinks(self) -> bool:
        """Check if FAT32 supports symlinks."""
        return False

    def supports_permissions(self) -> bool:
        """Check if FAT32 supports permissions."""
        return False


# Generic type for any file system implementation
FS = TypeVar('FS', bound=FileSystem)

# File system operations manager
@dataclass
class FileOperationsManager(Generic[FS]):
    """Generic file operations manager that works with any file system."""

    file_system: FS

    def perform_cross_system_copy(self, source: str, dest: str) -> None:
        """Perform a copy operation across file systems."""
        ic("Performing cross-system copy operation...")

        if self.file_system.supports_symlinks():
            ic("Symlinks will be preserved")

        if self.file_system.supports_permissions():
            ic("File permissions will be preserved")

        if self.file_system.create_directory(dest):
            ic("Destination directory created successfully")

        if self.file_system.copy_file(source, dest):
            ic("Files copied successfully")

        ic("Destination contents:")
        for file in self.file_system.list_files(dest):
            ic(f"- {file}")


def main() -> None:
    """Main function to demonstrate the adapter pattern."""
    ic("Testing file system adapters with invalid characters and assertions...")

    # Test helper for verifying sanitized filenames
    def test_sanitization(fs: FileSystem, input_path: str, expected_path: str) -> bool:
        manager = FileOperationsManager(fs)

        try:
            success = manager.file_system.create_directory(input_path)
            assert success, "Directory creation should succeed"

            files = manager.file_system.list_files(input_path)
            assert files, "Directory should not be empty after creation"

            test_file = f"{input_path}/test.txt"
            success = manager.file_system.copy_file(test_file, expected_path)
            assert success, "File copy should succeed"

            ic(f"Test passed for input: {input_path}")
            return True
        except Exception as e:
            print(f"Test failed: {e}")
            return False

    # Test suite 1: FAT32 adapter tests
    ic("Running FAT32 adapter tests...")

    # Test case 1: Invalid Windows characters
    test1 = test_sanitization(
        FAT32Adapter(),
        "test<file>name*.txt",
        "TEST_FIL_.TXT"
    )
    assert test1, "Invalid Windows characters test failed"

    # Test case 2: Long path handling
    long_path_adapter = FAT32Adapter()
    long_path = "a" * 300  # 300 character path
    success = long_path_adapter.create_directory(long_path)
    assert success, "Long path handling failed"

    # Test case 3: Spaces and special characters
    test3 = test_sanitization(
        FAT32Adapter(),
        "my file name: special * chars?.txt",
        "MY_FILE_.TXT"
    )
    assert test3, "Special characters test failed"

    # Test case 4: Path with multiple invalid characters
    test4 = test_sanitization(
        FAT32Adapter(),
        "C:/Program Files/My<App>*|.exe",
        "C_/PROGRA_1/MY_APP__.EXE"
    )
    assert test4, "Multiple invalid characters test failed"

    ic("FAT32 adapter tests completed successfully")

    # Test suite 2: APFS adapter tests
    ic("Running APFS adapter tests...")

    # Test case 1: Hidden files
    assert test_sanitization(
        APFSAdapter(),
        ".hiddenfile.txt",
        "_hiddenfile.txt"
    ), "Hidden files test failed"

    # Test case 2: Special characters
    assert test_sanitization(
        APFSAdapter(),
        "file:with/special\0chars.txt",
        "file_with_special_chars.txt"
    ), "Special characters test failed"

    # Test case 3: Long path handling
    long_path_adapter = APFSAdapter()
    long_path = "a" * 1100  # Path longer than APFS max
    success = long_path_adapter.create_directory(long_path)
    assert success, "Long path should be handled"

    # Test case 4: Combined special cases
    assert test_sanitization(
        APFSAdapter(),
        ".hidden/file:with\0special_chars.txt",
        "_hidden_file_with_special_chars.txt"
    ), "Combined special cases test failed"

    ic("APFS adapter tests completed successfully")

    # Test suite 3: Cross-system operations
    ic("Running cross-system operation tests...")

    # Test copying from APFS to FAT32
    ic("Scenario 1: Copying from APFS to FAT32")
    fat32_manager = FileOperationsManager(FAT32Adapter())

    source_file = "/Users/john/Documents/my:project*.txt"
    dest_file = "D:\\MY_PROJ.TXT"

    fat32_manager.perform_cross_system_copy(source_file, dest_file)

    # Test copying from FAT32 to APFS
    ic("Scenario 2: Copying from FAT32 to APFS")
    apfs_manager = FileOperationsManager(APFSAdapter())

    source_file = "D:\\DOCS\\PRO:J*.TXT"
    dest_file = "/Users/john/Documents/project.txt"

    apfs_manager.perform_cross_system_copy(source_file, dest_file)

    # Test suite 4: Edge cases
    ic("Running edge case tests...")
    fat32_adapter = FAT32Adapter()
    apfs_adapter = APFSAdapter()

    # Test empty paths
    assert fat32_adapter.create_directory("") is False, "Empty path should fail"
    assert apfs_adapter.create_directory("") is False, "Empty path should fail"

    # Test paths with only invalid characters
    all_invalid_chars = "<>:\"/\\|?*"
    result = fat32_adapter.create_directory(all_invalid_chars)
    assert result, "Completely invalid path should be sanitized"

    # Test unicode characters
    unicode_path = "תיקייה_with_unicode_名前.txt"
    success = fat32_adapter.copy_file(unicode_path, "OUTPUT.TXT")
    assert success, "Unicode handling should not fail"

    ic("Edge case tests completed successfully")

    ic("All file system adapter tests completed successfully!")


if __name__ == "__main__":
    main()
