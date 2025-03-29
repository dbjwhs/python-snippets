# Barrier Pattern Implementation in Python

## Overview
The Barrier Pattern is a synchronization mechanism used in concurrent programming to ensure that multiple threads wait for each other to reach a specific point before any of them can proceed further. It's like establishing a checkpoint where all threads must arrive before the race can continue.

## Real-World Use Cases

### 1. Parallel Matrix Computation
When computing large matrices in parallel, each thread might handle a portion of the matrix. Before moving to the next phase of computation, all threads need to complete their current phase to ensure data consistency.

```
Thread 1: [Computing A1] → [Barrier Wait] → [Computing B1]
Thread 2: [Computing A2] → [Barrier Wait] → [Computing B2]
Thread 3: [Computing A3] → [Barrier Wait] → [Computing B3]
```

### 2. Game Physics Engine
In a game physics engine, different threads might handle different aspects of the simulation:
- Thread 1: Position updates
- Thread 2: Collision detection
- Thread 3: Force calculations

All these computations must complete before moving to the next frame to maintain simulation accuracy.

### 3. Image Processing Pipeline
When processing images in parallel:
```
Stage 1: Multiple threads apply filters
Stage 2: All threads wait at barrier
Stage 3: Threads proceed with edge detection
Stage 4: All threads wait at barrier
Stage 5: Final composition
```

## Implementation Details

This repository provides two implementations of the Barrier Pattern:

### 1. Modern Implementation
Uses Python's standard library `threading.Barrier` class via a simple wrapper, which provides a clean and efficient implementation:

```python
from barrier_example.barrier import ModernBarrier

barrier = ModernBarrier(num_threads)
# ... in thread function:
barrier.wait()
```

Key features:
- Thread-safe by design
- Optimized performance
- Clear, modern syntax
- Automatic reset after all threads arrive

### 2. Custom Implementation
A manual implementation using traditional synchronization primitives:
- Uses `threading.Lock` and `threading.Condition`
- Maintains internal counter and phase
- Demonstrates the underlying mechanics of a barrier

```python
class CustomBarrier:
    def __init__(self, count: int) -> None:
        self._thread_count: int = count
        self._counter: int = count
        # ... other members

    def wait(self) -> None:
        # Implementation using condition variables
        ...
```

### A special note on condition variable usage

```python
self._condition.wait_for(lambda: phase_copy != self._phase)
```

This line of code is part of the condition variable wait operation:

1. `self._condition.wait_for()` - This is calling the wait_for method on our condition variable
2. It takes a lambda function that serves as the predicate/condition to check
3. The lambda checks if the stored phase_copy is different from the current self._phase
4. This indicates that the barrier has moved to a new phase

The line essentially means:
- Wait until the barrier's phase changes
- While waiting, release the lock so other threads can proceed
- The condition is checked whenever the condition variable is notified
- When the condition becomes true (phase has changed), continue execution

This is part of the barrier mechanism because:
1. When the last thread arrives, it changes self._phase
2. This makes the condition true for all waiting threads
3. All waiting threads can then proceed to the next phase

The use of phase_copy helps avoid the "spurious wakeup" problem by ensuring each thread only proceeds when the barrier has genuinely moved to a new phase, rather than just when it receives a notification.

As we can see with Python's `threading.Barrier`, things are a little easier than implementing it manually.

## Usage Example

```python
from barrier_example.examples import CustomBarrierExample, ModernBarrierExample
from barrier_example.examples import IceCreamLogger

NUM_THREADS = 4
logger = IceCreamLogger()

# Using modern barrier
ModernBarrierExample.demonstrate(NUM_THREADS, logger)

# Using custom barrier
CustomBarrierExample.demonstrate(NUM_THREADS, logger)
```

## Code Style Conventions
This implementation follows these coding conventions:
- Class member variables are prefixed with `_`
- Type annotations are used throughout the code (PEP 484)
- Final classes are marked with `@final` decorator
- Protocol classes are used for interfaces

## Running the Example

### Prerequisites
- Python 3.12 or higher
- uv package manager (recommended) or pip

### Quick Start (using the launcher script)
```bash
# Make the script executable if needed
chmod +x barrier_example_run.py

# Run the example
./barrier_example_run.py
```

### Installation
```bash
# Create a virtual environment with uv
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix/MacOS
.venv\\Scripts\\activate   # On Windows

# Install the package with development dependencies
uv pip install -e ".[dev]"
```

### Running the Example via Python Module
```bash
python -m barrier_example
```

### Running Tests
```bash
pytest
```

### Linting & Type Checking
```bash
ruff check .
ruff format .
mypy .
```

## Output Example
```
ic| 'Demonstrating modern barrier implementation:'
ic| 'Thread 0 completed phase 1'
ic| 'Thread 2 completed phase 1'
ic| 'Thread 1 completed phase 1'
ic| 'Thread 3 completed phase 1'
ic| 'Thread 0 starting phase 2'
ic| 'Thread 2 starting phase 2'
ic| 'Thread 1 starting phase 2'
ic| 'Thread 3 starting phase 2'
...
```

## Thread Safety
Both implementations are thread-safe and provide the following guarantees:
- All threads will wait until the last thread arrives
- No thread can proceed until all threads have arrived
- The barrier automatically resets for the next phase

## Performance Considerations
- The modern `threading.Barrier` implementation is generally more efficient
- The custom implementation might have more overhead due to lock and condition variable operations
- Both implementations scale well with the number of threads

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! Please feel free to submit pull requests with improvements or bug fixes.