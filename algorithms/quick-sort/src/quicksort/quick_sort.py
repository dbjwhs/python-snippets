"""
QuickSort implementation based on the Lomuto partition scheme.

This module provides a class-based implementation of the QuickSort algorithm,
featuring depth control, tail recursion optimization, and thorough type annotations.
"""

# MIT License
# Copyright (c) 2025 dbjwhs

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from icecream import ic

T = TypeVar('T', bound=int)  # Type variable for generics, bound to int


class Logger:
    """Singleton logger class for consistent log output."""

    _instance: Logger | None = None

    def __new__(cls) -> Logger:
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def log(level: str, message: str) -> None:
        """Log a message with the specified level."""
        ic(f"[{level}] {message}")


@dataclass
class RandomGenerator:
    """Generates random integers within a specified range."""

    min_value: int
    max_value: int
    _rng: random.Random = field(default_factory=lambda: random.Random(), init=False, repr=False)

    def get_number(self) -> int:
        """Return a random integer within the configured range."""
        return self._rng.randint(self.min_value, self.max_value)


@dataclass
class QuickSort(Generic[T]):
    """
    QuickSort implementation using the Lomuto partition scheme.

    This implementation features:
    - Classic Lomuto partition with last element as pivot
    - Depth control to prevent stack overflow
    - Tail recursion optimization
    - Generic typing for flexibility
    """

    array: list[T] = field(default_factory=list)

    def partition(self, low: int, high: int) -> int:
        """
        Partition the array and return the pivot index.

        Args:
            low: Starting index of partition
            high: Ending index of partition

        Returns:
            Index of the pivot after partitioning
        """
        pivot = self.array[high]
        i = low - 1

        for j in range(low, high):
            if self.array[j] <= pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]

        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        return i + 1

    def quick_sort_recursive(self, low: int, high: int, depth: int = 0) -> None:
        """
        Recursive quicksort implementation with depth control.

        Depth control is critical for preventing stack overflow in recursive functions
        and provides graceful degradation for pathological inputs.

        Args:
            low: Starting index of the array segment to sort
            high: Ending index of the array segment to sort
            depth: Current recursion depth (used for safety checks)
        """
        # Adjust max_depth per your needs
        max_depth = 10000

        while low < high:
            if depth >= max_depth:
                # Fall back to standard Python sort for very deep recursions
                self.array[low:high + 1] = sorted(self.array[low:high + 1])
                return

            # Partition and get pivot index
            pivot_index = self.partition(low, high)

            # Optimize tail recursion by handling smaller partition first
            if pivot_index - low < high - pivot_index:
                # Handle smaller partition with recursion
                if pivot_index > 0:  # Check to prevent underflow
                    self.quick_sort_recursive(low, pivot_index - 1, depth + 1)
                # Handle larger partition with loop continuation (tail recursion optimization)
                low = pivot_index + 1
            else:
                # Handle larger partition with recursion
                self.quick_sort_recursive(pivot_index + 1, high, depth + 1)
                # Handle smaller partition with loop continuation (tail recursion optimization)
                if pivot_index > 0:  # Check to prevent underflow
                    high = pivot_index - 1
                else:
                    break
            depth += 1

    def sort(self) -> None:
        """
        Public sort interface.

        Sorts the array in-place using the QuickSort algorithm.
        Empty arrays and single-element arrays are already considered sorted.
        """
        if len(self.array) <= 1:
            return
        self.quick_sort_recursive(0, len(self.array) - 1)

    def get_sorted_array(self) -> list[T]:
        """
        Get the sorted array.

        Returns:
            A copy of the sorted array
        """
        return self.array.copy()


def is_sorted(arr: list[int]) -> bool:
    """
    Check if an array is sorted in ascending order.

    Args:
        arr: List to check for sortedness

    Returns:
        True if array is sorted, False otherwise
    """
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def generate_random_vector(size: int) -> list[int]:
    """
    Generate a random vector of integers.

    Args:
        size: Size of the vector to generate

    Returns:
        List containing random integers
    """
    random_gen = RandomGenerator(-10000, 10000)
    return [random_gen.get_number() for _ in range(size)]


def main() -> None:
    """
    Run example sorting operations with QuickSort.

    This function demonstrates usage of the QuickSort class with
    various input arrays.
    """
    logger = Logger()
    logger.log("INFO", "Starting QuickSort demonstration")

    # Example of basic usage
    array = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    logger.log("INFO", f"Original array: {array}")

    sorter = QuickSort(array)
    sorter.sort()

    sorted_array = sorter.get_sorted_array()
    logger.log("INFO", f"Sorted array: {sorted_array}")

    # Verify the result
    assert is_sorted(sorted_array)
    logger.log("INFO", "Sorting successful!")

    # Example with large random array
    large_array = generate_random_vector(1000)
    large_sorter = QuickSort(large_array)
    large_sorter.sort()
    assert is_sorted(large_sorter.get_sorted_array())
    logger.log("INFO", "Large array sorting successful!")


if __name__ == "__main__":
    main()
