# MIT License
# Copyright (c) 2025 dbjwhs

"""Advanced negative space programming example.

Demonstrates more complex applications of negative space programming
using a generic container with customizable constraints.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from icecream import ic


@dataclass
class NegativeSpaceContainer:
    """A generic container that validates items using negative space principles.
    
    This container specifies what is NOT allowed rather than what is allowed.
    """
    
    # A list of constraint functions that items must NOT satisfy
    constraints: list[Callable[[Any], bool]] = field(default_factory=list)
    
    # The collection of items
    items: list[Any] = field(default_factory=list)
    
    def add_item(self, item: Any) -> None:
        """Add an item to the container if it doesn't violate any constraints.
        
        Args:
            item: The item to add
            
        Raises:
            ValueError: If the item violates any constraints

        """
        # Check all constraints (negative space validation)
        for i, constraint in enumerate(self.constraints):
            if constraint(item):
                ic(f"Item violates constraint #{i}")
                raise ValueError(f"Item violates constraint #{i}")
        
        # If we haven't thrown by now, the item is valid
        self.items.append(item)
        ic(f"Added item: {item}")
    
    def add_constraint(self, constraint: Callable[[Any], bool]) -> None:
        """Add a new constraint function.
        
        Args:
            constraint: A function that returns True if the item is invalid

        """
        self.constraints.append(constraint)
        ic(f"Added constraint #{len(self.constraints) - 1}")
        
        # Check all existing items against the new constraint
        # and remove any that violate it
        items_to_remove = []
        for item in self.items:
            if constraint(item):
                items_to_remove.append(item)
        
        for item in items_to_remove:
            self.items.remove(item)
            ic(f"Removed item {item} due to new constraint")


def main() -> None:
    """Demonstrate the NegativeSpaceContainer with various constraints."""
    ic("Starting NegativeSpaceContainer demonstration")
    
    # Create a container for integers with constraints
    int_container = NegativeSpaceContainer()
    
    # Add constraints: no negative numbers, no numbers above 100, no prime numbers
    int_container.add_constraint(lambda x: x < 0)  # No negative numbers
    int_container.add_constraint(lambda x: x > 100)  # No numbers above 100
    
    # Add some valid numbers
    for i in [0, 4, 6, 8, 10, 12, 50, 100]:
        try:
            int_container.add_item(i)
        except ValueError as e:
            ic(f"Error adding {i}: {e}")
    
    # Try adding some invalid numbers
    for i in [-5, 200]:
        try:
            int_container.add_item(i)
        except ValueError as e:
            ic(f"Error adding {i} (expected): {e}")
    
    # Define a function to check if a number is prime
    def is_prime(n: int) -> bool:
        """Return True if n is a prime number."""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    # Add a new constraint: no prime numbers
    int_container.add_constraint(is_prime)
    
    # Try adding prime numbers (should fail)
    for i in [2, 3, 5, 7, 11, 13]:
        try:
            int_container.add_item(i)
        except ValueError as e:
            ic(f"Error adding {i} (expected): {e}")
    
    # Create a container for strings with constraints
    string_container = NegativeSpaceContainer()
    
    # Add constraints: no empty strings, no strings longer than 10 chars
    string_container.add_constraint(lambda s: not s)  # No empty strings
    string_container.add_constraint(lambda s: len(s) > 10)  # No strings longer than 10
    
    # Add some valid strings
    for s in ["Hello", "World", "Python"]:
        try:
            string_container.add_item(s)
        except ValueError as e:
            ic(f"Error adding '{s}': {e}")
    
    # Try adding some invalid strings
    for s in ["", "This is too long"]:
        try:
            string_container.add_item(s)
        except ValueError as e:
            ic(f"Error adding '{s}' (expected): {e}")
    
    ic("NegativeSpaceContainer demonstration completed")


if __name__ == "__main__":
    main()