# Modern Python Thread Pool Implementation

## Overview
This repository contains a modern Python implementation of a thread pool pattern. The thread pool manages a collection of worker threads that can execute tasks asynchronously, providing an efficient way to parallelize work across multiple threads.

## Features
- Modern Python 3.12+ implementation with type hints
- Thread-safe task queue
- Asynchronous task execution
- Future-based result handling
- Exception-safe design
- Automatic thread management
- Clean shutdown mechanism

## Requirements
- Python 3.12 or later
- icecream (for logging)
- uv (for package management)
- ruff (for linting)
- pytest (for testing)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd thread-pool

# Create a virtual environment using uv
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# .venv\Scripts\activate  # On Windows

# Install the package and its dependencies
uv pip install -e .
```

## Usage Examples

### Basic Usage

```python
from thread_pool import ThreadPool, Logger, LogLevel

# Get the logger instance
logger = Logger.get_instance()

# Create a thread pool with 4 threads
pool = ThreadPool(4, logger)

# Example 1: Enqueue a lambda
future1 = pool.enqueue(lambda x: x * x, 42)
result1 = future1.result()  # Returns 1764

# Example 2: Enqueue a function
def multiply(x, y):
    return x * y

future2 = pool.enqueue(multiply, 3.14, 2.0)
result2 = future2.result()  # Returns 6.28

# Don't forget to shut down the pool when you're done
pool.shutdown()
```

### Parallel Processing Example

```python
import time
from thread_pool import ThreadPool, Logger, LogLevel

logger = Logger.get_instance()
pool = ThreadPool(4, logger)

# Process a list in parallel
items = list(range(10))

def process_item(item):
    logger.log(LogLevel.INFO, f"Processing item {item}")
    time.sleep(1)  # Simulate work
    return item * 10

# Submit all items for processing
futures = [pool.enqueue(process_item, item) for item in items]

# Collect results as they complete
results = [future.result() for future in futures]
print(f"Results: {results}")

pool.shutdown()
```

## Implementation Details

### Class Structure
The `ThreadPool` class consists of the following key components:

```python
class ThreadPool:
    def __init__(self, num_threads: int, logger: Logger) -> None:
        self._workers: List[Thread] = []
        self._tasks: Queue[Callable[[], None]] = Queue()
        self._queue_mutex: Lock = Lock()
        self._condition: Condition = Condition(self._queue_mutex)
        self._stop: bool = False
        self._logger: Logger = logger
        # ...
```

### Key Components

1. **Worker Threads**
    - Stored in a List of Threads
    - Created during thread pool initialization
    - Continuously wait for and execute tasks
    - Automatically join on destruction

2. **Task Queue**
    - Uses Python's Queue implementation
    - Thread-safe implementation
    - Stores pending tasks
    - FIFO (First In, First Out) processing

3. **Synchronization Mechanisms**
    - Mutex for thread-safe queue access
    - Condition variable for thread notification
    - Stop flag for clean shutdown

### Future-based Result Handling

The `enqueue` method returns a `Future` object that allows asynchronous access to the task's result:

```python
def enqueue(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> Future[T]:
    future: Future[T] = concurrent.futures.Future()
    
    def task_wrapper() -> None:
        if future.cancelled():
            return
            
        try:
            result = func(*args, **kwargs)
            future.set_result(result)
        except Exception as e:
            future.set_exception(e)
    
    # Enqueue the task wrapper
    with self._queue_mutex:
        if self._stop:
            raise RuntimeError("Cannot enqueue on stopped ThreadPool")
        
        self._tasks.put(task_wrapper)
        self._logger.log(LogLevel.INFO, "Task enqueued")
    
    # Notify one waiting thread
    with self._condition:
        self._condition.notify()
    
    return future
```

## Running the Examples

The package includes several examples demonstrating different usage patterns:

```bash
# Run the basic usage example
./examples/basic_usage.py

# Run the advanced usage example
./examples/advanced_usage.py

# Run the package directly
python -m thread_pool

# Use the launcher script
./run_thread_pool.py
```

## Running Tests

The package includes comprehensive pytest tests:

```bash
# Run the tests
pytest

# Run the tests with coverage
pytest --cov=thread_pool
```

## Advanced Features

1. **Task Enqueuing**
   - Supports any callable with any arguments
   - Returns a Future for result handling
   - Exception safety
   - Task cancellation support

2. **Exception Handling**
   - Exception-safe task execution
   - Error propagation through futures
   - Safe thread pool shutdown
   - Runtime error detection for stopped pools

3. **Thread Safety**
   - Mutex-protected task queue access
   - Condition variable for thread synchronization
   - Safe task enqueuing and execution

## Performance Considerations

1. **Task Granularity**
   - Best for compute-intensive tasks
   - Avoid very short tasks due to overhead
   - Consider task batching for small operations

2. **Thread Count**
   - Default to CPU count
   - Adjust based on workload characteristics
   - Consider system resources and context

## Best Practices

1. **Resource Management**
   - Create thread pool with appropriate thread count
   - Ensure proper shutdown
   - Handle exceptions appropriately

2. **Task Design**
   - Make tasks independent
   - Avoid shared state when possible
   - Use appropriate synchronization when needed

3. **Error Handling**
   - Check futures for exceptions
   - Handle pool shutdown gracefully
   - Implement appropriate error recovery

## License
This implementation is provided under the MIT License.

## Contributing
Contributions are welcome! Please feel free to submit pull requests with improvements or bug fixes.