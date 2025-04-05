#!/usr/bin/env python3
"""Tests for the slicing module."""

import pickle
from copy import copy
from unittest.mock import patch

from slicing import Derived, ImproperInheritance


def test_base_derived_initialization() -> None:
    """Test that Base and Derived classes initialize properly."""
    derived = Derived()
    assert derived.base_data == "Modified base data"
    assert derived.derived_data == "Derived data"


def test_process_by_reference() -> None:
    """Test that processing by reference preserves the object's type."""
    derived = Derived()

    # Patch the logger to capture output
    with patch("slicing.slicing.Logger.info") as mock_info:
        # Call the function
        from slicing.slicing import process_by_reference
        process_by_reference(derived)

        # Verify the correct method was called
        assert any("Derived with:" in call.args[0] for call in mock_info.call_args_list)


def test_process_with_copy() -> None:
    """Test copying behavior with derived classes."""
    derived = Derived()
    copied = copy(derived)

    # In Python, shallow copy should preserve class identity
    assert isinstance(copied, Derived)
    assert copied.base_data == "Modified base data"
    assert copied.derived_data == "Derived data"


def test_improper_inheritance() -> None:
    """Test that improper inheritance doesn't initialize properly."""
    improper = ImproperInheritance()

    # Base data is initialized because Base.__init__ is called directly
    assert improper.base_data == "Base data"

    # improper_data is initialized in ImproperInheritance.__init__
    assert improper.improper_data == "Improper data"

    # derived_data is not initialized because Derived.__init__ is skipped
    assert not hasattr(improper, "derived_data")


def test_serialization() -> None:
    """Test serialization and deserialization of objects."""
    derived = Derived()
    serialized = pickle.dumps(derived)
    restored = pickle.loads(serialized)

    # Verify the object maintains its type and data
    assert isinstance(restored, Derived)
    assert restored.base_data == "Modified base data"
    assert restored.derived_data == "Derived data"

    # Ensure we can still call methods
    assert hasattr(restored, "print")
    assert callable(restored.print)
