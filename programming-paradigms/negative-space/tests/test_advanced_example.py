# MIT License
# Copyright (c) 2025 dbjwhs

"""Unit tests for the advanced negative space example.

Tests the NegativeSpaceContainer class functionality.
"""

import pytest

from negative_space.examples.advanced_example import NegativeSpaceContainer


class TestNegativeSpaceContainer:
    """Test suite for the NegativeSpaceContainer class."""
    
    def test_valid_item(self) -> None:
        """Test that a valid item is accepted."""
        container = NegativeSpaceContainer()
        # No constraints yet, so any item should be valid
        container.add_item(42)
        assert 42 in container.items
    
    def test_constraint_violation(self) -> None:
        """Test that an item violating a constraint is rejected."""
        container = NegativeSpaceContainer()
        # Add constraint: no negative numbers
        container.add_constraint(lambda x: x < 0)
        
        # Add a valid item
        container.add_item(42)
        assert 42 in container.items
        
        # Add an invalid item
        with pytest.raises(ValueError):
            container.add_item(-1)
    
    def test_multiple_constraints(self) -> None:
        """Test that multiple constraints are checked."""
        container = NegativeSpaceContainer()
        # Add constraints: no negative numbers, no numbers above 100
        container.add_constraint(lambda x: x < 0)
        container.add_constraint(lambda x: x > 100)
        
        # Add valid items
        for i in [0, 50, 100]:
            container.add_item(i)
            assert i in container.items
        
        # Add invalid items
        for i in [-1, 101]:
            with pytest.raises(ValueError):
                container.add_item(i)
    
    def test_add_constraint_removes_violating_items(self) -> None:
        """Test that adding a new constraint removes violating items."""
        container = NegativeSpaceContainer()
        
        # Add some items
        for i in [1, 2, 3, 4, 5]:
            container.add_item(i)
        
        # Add constraint: no odd numbers
        container.add_constraint(lambda x: x % 2 == 1)
        
        # Check that odd numbers were removed
        assert container.items == [2, 4]
    
    def test_generic_constraints(self) -> None:
        """Test that the container works with different types of items."""
        container = NegativeSpaceContainer()
        
        # Add constraint: no empty strings
        container.add_constraint(lambda s: isinstance(s, str) and not s)
        
        # Add valid strings
        container.add_item("Hello")
        container.add_item("World")
        
        # Try adding an empty string
        with pytest.raises(ValueError):
            container.add_item("")
        
        # Numbers should still be valid
        container.add_item(42)
        
        # Add constraint: no numbers
        container.add_constraint(lambda x: isinstance(x, int))
        
        # Check that numbers were removed
        assert 42 not in container.items
        
        # Check that strings remain
        assert "Hello" in container.items
        assert "World" in container.items