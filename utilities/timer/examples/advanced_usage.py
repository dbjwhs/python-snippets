#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""Advanced usage examples for HighResolutionTimer."""

import statistics
import time
import types

from timer_py import HighResolutionTimer


def simulate_work(duration_ms: float) -> None:
    """
    Simulate work by sleeping for the specified duration.
    
    Args:
        duration_ms: Sleep duration in milliseconds
    """
    time.sleep(duration_ms / 1000)


def benchmark_function(func: callable, iterations: int = 5) -> list[float]:
    """
    Benchmark a function over multiple iterations.
    
    Args:
        func: Function to benchmark
        iterations: Number of iterations to run
        
    Returns:
        List of elapsed times in milliseconds
    """
    results = []
    timer = HighResolutionTimer()
    
    for i in range(iterations):
        timer.start()
        func()
        timer.stop()
        results.append(timer.elapsed_milliseconds())
        print(f"Iteration {i+1}: {timer.elapsed_formatted()}")
    
    return results


def print_statistics(results: list[float]) -> None:
    """
    Print statistics for benchmark results.
    
    Args:
        results: List of benchmark times in milliseconds
    """
    print("\nBenchmark Statistics:")
    print(f"  Iterations: {len(results)}")
    print(f"  Mean:       {statistics.mean(results):.3f} ms")
    print(f"  Median:     {statistics.median(results):.3f} ms")
    print(f"  Std Dev:    {statistics.stdev(results) if len(results) > 1 else 0:.3f} ms")
    print(f"  Min:        {min(results):.3f} ms")
    print(f"  Max:        {max(results):.3f} ms")


class TimedContextManager:
    """A context manager that times execution using HighResolutionTimer."""
    
    def __init__(self, name: str = "Operation") -> None:
        """
        Initialize context manager.
        
        Args:
            name: Name of the operation being timed
        """
        self.name = name
        self.timer = HighResolutionTimer()
    
    def __enter__(self) -> HighResolutionTimer:
        """Start timing when entering context."""
        self.timer.start()
        return self.timer
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Stop timing when exiting context and print results."""
        self.timer.stop()
        print(f"{self.name} took {self.timer.elapsed_formatted()}")


def main() -> None:
    """Run the advanced usage examples."""
    print("HighResolutionTimer Advanced Usage Examples")
    print("==========================================\n")
    
    # Example 1: Function benchmarking
    print("Example 1: Function benchmarking")
    print("--------------------------------")
    
    def test_function() -> None:
        """Test function that simulates variable work."""
        # Simulate work that varies slightly each time
        base_duration = 50  # ms
        variance = 10  # ms
        simulated_duration = base_duration + (hash(time.time()) % variance)
        simulate_work(simulated_duration)
    
    print("Benchmarking test_function over 5 iterations:")
    results = benchmark_function(test_function, 5)
    print_statistics(results)
    
    # Example 2: Using the timer as a context manager
    print("\nExample 2: Using the timer as a context manager")
    print("---------------------------------------------")
    
    print("Timing operations using context manager:")
    
    with TimedContextManager("Short operation") as timer:
        simulate_work(20)
        # Mid-operation timing check
        print(f"  Mid-operation timing: {timer.elapsed_formatted()}")
        simulate_work(30)
    
    with TimedContextManager("Medium operation"):
        simulate_work(100)
    
    with TimedContextManager("Long operation"):
        simulate_work(200)
    
    # Example 3: Cumulative timing
    print("\nExample 3: Cumulative timing")
    print("---------------------------")
    
    timer = HighResolutionTimer()
    
    print("Starting cumulative timing...")
    timer.start()
    
    for i in range(1, 4):
        simulate_work(50)
        print(f"After step {i}: {timer.elapsed_formatted()} elapsed")
    
    timer.stop()
    print(f"Total time: {timer.elapsed_formatted()}")


if __name__ == "__main__":
    main()