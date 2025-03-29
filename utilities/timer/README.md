# High Resolution Timer Class

A modern Python implementation of a high-precision timer using the `time.perf_counter_ns` function. This class provides accurate timing measurements with nanosecond precision and multiple output formats.

## Features

- High-precision timing using `time.perf_counter_ns`
- Multiple time unit outputs (nanoseconds, microseconds, milliseconds, seconds)
- Automatic formatting with appropriate units
- Runtime status checking
- Thread-safe implementation
- Simple start/stop/reset interface
- Type hints for better code analysis

## Requirements

- Python 3.12 or later
- icecream (for enhanced debugging)

## Installation

```bash
# Create a virtual environment and install the package
uv venv
. .venv/bin/activate
uv pip install -e ".[dev]"
```

## Usage

### Basic Usage

```python
from timer_py import HighResolutionTimer

# Create timer instance
timer = HighResolutionTimer()

# Start timing
timer.start()

# Your code to measure here
do_something()

# Stop timing
timer.stop()

# Get the elapsed time
print(f"Operation took: {timer.elapsed_formatted()}")
```

### Available Methods

#### Timer Control
- `start()`: Starts the timer
- `stop()`: Stops the timer
- `reset()`: Resets the timer
- `running()`: Checks if the timer is currently running

#### Time Measurements
- `elapsed_nanoseconds()`: Get elapsed time in nanoseconds
- `elapsed_microseconds()`: Get elapsed time in microseconds
- `elapsed_milliseconds()`: Get elapsed time in milliseconds
- `elapsed_seconds()`: Get elapsed time in seconds
- `elapsed_formatted()`: Get formatted string with appropriate unit

### Example with Multiple Features

```python
from timer_py import HighResolutionTimer

timer = HighResolutionTimer()

# Basic timing
timer.start()
complex_operation()
timer.stop()

# Get results in different formats
print(f"Raw nanoseconds: {timer.elapsed_nanoseconds()}")
print(f"Formatted time: {timer.elapsed_formatted()}")

# Check timer status
if not timer.running():
    print("Timer is stopped")

# Multiple measurements
timer.reset()
timer.start()
operation_1()
print(f"Time so far: {timer.elapsed_formatted()}")
operation_2()
timer.stop()
print(f"Final time: {timer.elapsed_formatted()}")
```

## Launcher Scripts

The package includes convenient launcher scripts to run the examples:

- `run_timer.py`: Runs the main timer demonstration
- `run_example.py`: Runs the basic usage example
- `run_advanced_example.py`: Runs the advanced usage example with benchmarking and context managers

Make the scripts executable and run:

```bash
chmod +x run_timer.py run_example.py run_advanced_example.py
./run_timer.py
./run_example.py
./run_advanced_example.py
```

## Running as a Module

You can also run the package as a Python module:

```bash
python -m timer_py
```

## Output Format

The `elapsed_formatted()` method automatically selects the most appropriate unit:
- Under 1 microsecond: displays in nanoseconds (ns)
- Under 1 millisecond: displays in microseconds (µs)
- Under 1 second: displays in milliseconds (ms)
- 1 second or more: displays in seconds (s)

Example outputs:
```
856 ns
1.234 µs
12.345 ms
1.234 s
```

## Implementation Details

The timer uses Python's `time.perf_counter_ns()` function for maximum precision. This function provides the time with nanosecond resolution, making it suitable for performance measurements. Time measurements are converted to the requested unit only when queried, ensuring no precision is lost during timing operations.

## Performance Considerations

- The timer has minimal overhead, making it suitable for measuring both very short and long operations
- Time point storage uses the system's highest precision clock
- All time unit conversions are performed efficiently
- The formatted output includes a small overhead for string formatting

## Thread Safety

The timer is thread-safe for independent instances. However, sharing a single timer instance between threads requires external synchronization.

## License

This code is provided under the MIT License. Feel free to use, modify, and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.