#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Script to manually fix linting issues found by ruff.

This script makes the necessary changes to fix linting issues found by ruff
that couldn't be automatically fixed.
"""

import os
import re
from pathlib import Path


def fix_reader_writer_file() -> None:
    """Fix linting issues in reader_writer.py."""
    file_path = Path("src/reader_writer/reader_writer.py")
    with open(file_path) as f:
        content = f.read()
    
    # Fix CONSTANT variable names to lowercase
    content = re.sub(r"READER_THREAD_CNT", "reader_thread_cnt", content)
    content = re.sub(r"WRITER_THREAD_CNT", "writer_thread_cnt", content)
    
    # Fix unused read_lock and write_lock variables
    content = re.sub(
        r"read_lock = ReadLock\(self\)",
        "_ = ReadLock(self)  # Variable keeps lock alive for method duration",
        content
    )
    content = re.sub(
        r"write_lock = WriteLock\(self\)",
        "_ = WriteLock(self)  # Variable keeps lock alive for method duration",
        content
    )
    
    # Fix unused loop variables
    content = re.sub(r"for reads in range", "for _ in range", content)
    
    with open(file_path, "w") as f:
        f.write(content)


def fix_utils_file() -> None:
    """Fix linting issues in utils.py."""
    file_path = Path("src/reader_writer/utils.py")
    with open(file_path) as f:
        content = f.read()
    
    # Fix super() call
    content = re.sub(
        r"super\(Logger, cls\).__new__\(cls\)",
        "super().__new__(cls)",
        content
    )
    
    # Fix string literals in exceptions
    content = re.sub(
        r'raise TypeError\("Copying of this object is not allowed"\)',
        'error_msg = "Copying of this object is not allowed"\n        raise TypeError(error_msg)',
        content
    )
    content = re.sub(
        r'raise TypeError\("Deep copying of this object is not allowed"\)',
        'error_msg = "Deep copying of this object is not allowed"\n        raise TypeError(error_msg)',
        content
    )
    
    with open(file_path, "w") as f:
        f.write(content)


def fix_examples_files() -> None:
    """Fix linting issues in example files."""
    # Fix basic_usage.py
    basic_path = Path("examples/basic_usage.py")
    with open(basic_path) as f:
        content = f.read()
    
    # Fix CONSTANT variable names to lowercase
    content = re.sub(r"READER_COUNT", "reader_count", content)
    content = re.sub(r"WRITER_COUNT", "writer_count", content)
    
    # Fix unused loop variables
    content = re.sub(r"for j in range", "for _ in range", content)
    
    with open(basic_path, "w") as f:
        f.write(content)
    
    # Fix advanced_usage.py
    advanced_path = Path("examples/advanced_usage.py")
    with open(advanced_path) as f:
        content = f.read()
    
    # Fix CONSTANT variable names to lowercase
    content = re.sub(r"READER_COUNT", "reader_count", content)
    content = re.sub(r"WRITER_COUNT", "writer_count", content)
    
    # Fix unused futures variables
    content = re.sub(
        r"reader_futures = \[",
        "# The futures variables are stored in the executor and don't need to be tracked\n        _ = [",
        content
    )
    content = re.sub(
        r"writer_futures = \[",
        "_ = [",
        content
    )
    
    with open(advanced_path, "w") as f:
        f.write(content)


def fix_test_files() -> None:
    """Fix linting issues in test files."""
    # Fix test_reader_writer.py
    test_path = Path("tests/test_reader_writer.py")
    with open(test_path) as f:
        content = f.read()
    
    # Fix CONSTANT variable names to lowercase
    content = re.sub(r"NUM_READERS", "num_readers", content)
    content = re.sub(r"NUM_WRITERS", "num_writers", content)
    
    # Fix magic number
    content = re.sub(
        r"assert readers_writers._shared_resource == 42",
        "expected_value = 42\n    assert readers_writers._shared_resource == expected_value",
        content
    )
    
    with open(test_path, "w") as f:
        f.write(content)
    
    # Fix test_utils.py
    test_utils_path = Path("tests/test_utils.py")
    with open(test_utils_path) as f:
        content = f.read()
    
    # Fix magic number
    content = re.sub(
        r"assert mock_ic.call_count == 4",
        "expected_calls = 4  # One for each log level\n        assert mock_ic.call_count == expected_calls",
        content
    )
    
    with open(test_utils_path, "w") as f:
        f.write(content)


def main() -> None:
    """Fix all linting issues."""
    # Change to the script's directory
    os.chdir(Path(__file__).parent)
    
    print("Applying linting fixes...")
    fix_reader_writer_file()
    fix_utils_file()
    fix_examples_files()
    fix_test_files()
    print("Linting fixes applied successfully.")


if __name__ == "__main__":
    main()