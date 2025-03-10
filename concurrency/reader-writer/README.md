# Python Readers-Writers Implementation

This project implements a thread-safe Readers-Writers synchronization mechanism in Python. The implementation features RAII-style context management, thread-safe logging using a singleton pattern, and prevention of writer starvation.

## Overview

The Readers-Writers problem is a classic synchronization challenge where multiple threads need to access a shared resource, with some threads reading the resource and others writing to it. The key constraints are:
- Multiple readers can access the resource simultaneously
- Only one writer can access the resource at a time
- When a writer is writing, no readers can access the resource
- All console output must be thread-safe

## Features

- Thread-safe implementation using modern Python concepts
- RAII-style pattern for automatic resource management
- Writer preference to prevent writer starvation
- Centralized thread-safe logging through singleton pattern
- Exception-safe design
- Comprehensive usage examples
- Fully typed with Python type annotations

## Installation

### Prerequisites

- Python 3.12 or higher
- `uv` package manager (recommended)

### Installing with uv

```bash
# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package and its dependencies
uv pip install -e .
```

## Quick Start

```python
import time
from threading import Thread

from reader_writer.reader_writer import ReadersWriters
from reader_writer.utils import LogLevel, Logger

# Get the singleton logger instance
logger = Logger.get_instance()

# Create a ReadersWriters instance
rw = ReadersWriters()

# Create reader thread
def reader_thread():
    logger.log(LogLevel.INFO, "Reader thread started")
    for _ in range(3):
        rw.read_resource(logger)
        time.sleep(0.1)
    logger.log(LogLevel.INFO, "Reader thread finished")

# Create writer thread
def writer_thread():
    logger.log(LogLevel.INFO, "Writer thread started")
    for i in range(3):
        rw.write_resource(i, logger)
        time.sleep(0.2)
    logger.log(LogLevel.INFO, "Writer thread finished")

# Start threads
threads = [
    Thread(target=reader_thread),
    Thread(target=writer_thread),
    Thread(target=reader_thread)
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

logger.log(LogLevel.INFO, "All threads completed")
```

## Running the Examples

The package comes with example scripts to demonstrate usage:

```bash
# Run the basic example
python run_basic_example.py

# Run the advanced example
python run_advanced_example.py

# Run through the module
python -m reader_writer
```

## Key Components

### Logger (Singleton)

A singleton class that provides thread-safe logging capabilities using the icecream package:

```python
class Logger:
    """Thread-safe singleton logger using icecream."""
    _instance: ClassVar[Optional["Logger"]] = None
    _lock: ClassVar[Lock] = Lock()

    @classmethod
    def get_instance(cls) -> "Logger":
        """Get the singleton instance of the logger."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def log(self, level: LogLevel, message: str) -> None:
        """Log a message with the specified log level."""
        with self._mutex:
            # Thread-safe logging using icecream
            ic(f"{level.name}: {message}")
```

### ReadersWriters Class

The main class implementing the synchronization mechanism:

#### Member Variables
- `_mutex`: Protects access to shared state
- `_read_cv`: Condition variable for reader synchronization
- `_write_cv`: Condition variable for writer synchronization
- `_active_readers`: Count of currently active readers
- `_waiting_readers`: Count of readers waiting to acquire access
- `_is_writing`: Flag indicating if a writer is currently active
- `_waiting_writers`: Count of writers waiting to acquire access
- `_shared_resource`: The protected resource

### RAII-Style Read/Write Locks

The ReadersWriters class uses inner classes for automatic lock management:

```python
def read_resource(self, logger: Logger) -> None:
    """Read the shared resource with a RAII-style read lock."""
    class ReadLock(NonCopyable):
        def __init__(self, rw: ReadersWriters) -> None:
            super().__init__()
            self._rw = rw
            self._rw.start_read()
            
        def __del__(self) -> None:
            self._rw.end_read()
    
    # Create a read lock that automatically acquires and releases the lock
    read_lock = ReadLock(self)
    
    # The lock is now acquired and will be automatically released
    # when read_lock goes out of scope
    logger.log(LogLevel.INFO, f"Reading resource: {self._shared_resource}")
    time.sleep(0.1)  # Simulate reading operation
```

## Advanced Usage

For more advanced usage, see the examples directory, particularly the `advanced_usage.py` file which demonstrates protecting a shared database with the ReadersWriters pattern.

## Testing

The project includes a comprehensive test suite:

```bash
# Run tests with pytest
pytest

# Run tests with coverage
pytest --cov=reader_writer
```

## Requirements

- Python 3.12 or later
- Dependencies listed in pyproject.toml

## License

This implementation is provided under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests with improvements or bug fixes.