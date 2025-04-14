#!/usr/bin/env python3
"""
Basic usage example for the QuickSort implementation.

This script demonstrates how to use the QuickSort class to sort
various types of arrays and verify the results.
"""


from quicksort.quick_sort import QuickSort, is_sorted


def main() -> None:
    """Demonstrate basic usage of the QuickSort class."""
    # Example 1: Basic sorting
    print("Example 1: Basic sorting")
    numbers: list[int] = [3, 1, 4, 1, 5, 9, 2, 6]
    sorter = QuickSort(numbers)
    sorter.sort()
    result = sorter.get_sorted_array()
    print("Original: [3, 1, 4, 1, 5, 9, 2, 6]")
    print(f"Sorted: {result}")
    print(f"Is sorted: {is_sorted(result)}")
    print()

    # Example 2: Already sorted array
    print("Example 2: Already sorted array")
    sorted_array: list[int] = [1, 2, 3, 4, 5]
    sorter = QuickSort(sorted_array)
    sorter.sort()
    result = sorter.get_sorted_array()
    print(f"Original: {sorted_array}")
    print(f"Sorted: {result}")
    print(f"Is sorted: {is_sorted(result)}")
    print()

    # Example 3: Reverse sorted array
    print("Example 3: Reverse sorted array")
    reverse_array: list[int] = [5, 4, 3, 2, 1]
    sorter = QuickSort(reverse_array)
    sorter.sort()
    result = sorter.get_sorted_array()
    print(f"Original: {reverse_array}")
    print(f"Sorted: {result}")
    print(f"Is sorted: {is_sorted(result)}")
    print()

    # Example 4: Array with duplicates
    print("Example 4: Array with duplicates")
    duplicates: list[int] = [3, 1, 3, 1, 3, 1]
    sorter = QuickSort(duplicates)
    sorter.sort()
    result = sorter.get_sorted_array()
    print(f"Original: {duplicates}")
    print(f"Sorted: {result}")
    print(f"Is sorted: {is_sorted(result)}")
    print()

    # Example 5: Array with negative numbers
    print("Example 5: Array with negative numbers")
    negative_numbers: list[int] = [-5, 3, -2, 7, -1, 0, 4]
    sorter = QuickSort(negative_numbers)
    sorter.sort()
    result = sorter.get_sorted_array()
    print(f"Original: {negative_numbers}")
    print(f"Sorted: {result}")
    print(f"Is sorted: {is_sorted(result)}")


if __name__ == "__main__":
    main()
