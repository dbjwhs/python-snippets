"""
Tests for the QuickSort implementation.

These tests verify the functionality of the QuickSort class against various input cases,
including edge cases and random data.
"""



from quicksort.quick_sort import QuickSort, generate_random_vector, is_sorted


def test_empty_array() -> None:
    """Test sorting an empty array."""
    empty_array: list[int] = []
    qs = QuickSort(empty_array)
    qs.sort()
    assert qs.get_sorted_array() == []


def test_single_element() -> None:
    """Test sorting an array with a single element."""
    single_element = [42]
    qs = QuickSort(single_element)
    qs.sort()
    assert qs.get_sorted_array() == [42]


def test_already_sorted() -> None:
    """Test sorting an already sorted array."""
    sorted_array = [1, 2, 3, 4, 5]
    qs = QuickSort(sorted_array)
    qs.sort()
    assert is_sorted(qs.get_sorted_array())
    assert qs.get_sorted_array() == [1, 2, 3, 4, 5]


def test_reverse_sorted() -> None:
    """Test sorting a reverse-sorted array."""
    reverse_sorted = [5, 4, 3, 2, 1]
    qs = QuickSort(reverse_sorted)
    qs.sort()
    assert is_sorted(qs.get_sorted_array())
    assert qs.get_sorted_array() == [1, 2, 3, 4, 5]


def test_duplicates() -> None:
    """Test sorting an array with duplicate elements."""
    duplicates = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    qs = QuickSort(duplicates)
    qs.sort()
    assert is_sorted(qs.get_sorted_array())
    assert qs.get_sorted_array() == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]


def test_large_random() -> None:
    """Test sorting a large random array."""
    large_random = generate_random_vector(1000)
    qs = QuickSort(large_random)
    qs.sort()
    assert is_sorted(qs.get_sorted_array())


def test_negative_numbers() -> None:
    """Test sorting an array with negative numbers."""
    negative_numbers = [-5, 3, -2, 7, -1, 0, 4]
    qs = QuickSort(negative_numbers)
    qs.sort()
    assert is_sorted(qs.get_sorted_array())
    assert qs.get_sorted_array() == [-5, -2, -1, 0, 3, 4, 7]


def test_all_same_values() -> None:
    """Test sorting an array where all elements have the same value."""
    same_values = [42, 42, 42, 42, 42]
    qs = QuickSort(same_values)
    qs.sort()
    assert is_sorted(qs.get_sorted_array())
    assert qs.get_sorted_array() == [42, 42, 42, 42, 42]


def test_array_modification() -> None:
    """Test that the original array is modified by the sort operation."""
    array = [3, 1, 4, 1, 5]
    qs = QuickSort(array)
    qs.sort()
    assert qs.array == [1, 1, 3, 4, 5]  # Check the internal array is modified


def test_get_sorted_array_returns_copy() -> None:
    """Test that get_sorted_array returns a copy of the array."""
    array = [3, 1, 4, 1, 5]
    qs = QuickSort(array)
    qs.sort()
    sorted_array = qs.get_sorted_array()

    # Modify the returned array
    sorted_array[0] = 999

    # Original array in the class should remain unchanged
    assert qs.array[0] == 1
