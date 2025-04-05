#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""Demonstration of Python object copying pitfalls analogous to C++ object slicing.

While Python doesn't have object slicing in the same way as C++, this module
demonstrates similar issues that occur when copying objects improperly,
using super() incorrectly, or during serialization/deserialization.
"""

import pickle
from abc import ABC, abstractmethod
from copy import copy

from icecream import ic


class Logger:
    """Simple singleton logger class."""

    _instance = None

    def __new__(cls) -> "Logger":
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def info(message: str) -> None:
        """Log an info message."""
        ic(message)


class Base(ABC):
    """Base class demonstrating potential slicing issues."""

    def __init__(self) -> None:
        """Initialize the base class."""
        self.base_data: str = "Base data"

    @abstractmethod
    def print(self) -> None:
        """Print information about the object."""
        pass


class Derived(Base):
    """Derived class with additional data."""

    def __init__(self) -> None:
        """Initialize the derived class."""
        super().__init__()
        self.derived_data: str = "Derived data"
        self.base_data = "Modified base data"

    def print(self) -> None:
        """Print information about the derived object."""
        Logger().info(f"Derived with: {self.base_data} and {self.derived_data}")


# Case 1: By reference - SAFE, Python always uses references
def process_by_reference(obj: Base) -> None:
    """Process the object by reference (default in Python)."""
    Logger().info("Processing by reference: ")
    obj.print()


# Case 2: Improper copying - DANGEROUS
def process_with_copy(obj: Base) -> None:
    """Process a shallow copy of the object (can lead to issues)."""
    Logger().info("Processing with shallow copy: ")
    obj_copy = copy(obj)
    obj_copy.print()  # May lose derived data depending on the implementation


# Case 3: Improper inheritance - DANGEROUS
class ImproperInheritance(Derived):
    """Class demonstrating improper use of super()."""

    def __init__(self) -> None:
        """Initialize with improper super() call."""
        # This calls Base.__init__() directly, skipping Derived.__init__()
        Base.__init__(self)
        self.improper_data: str = "Improper data"

    def print(self) -> None:
        """Print information about the improper object."""
        # Will be missing derived_data initialization from Derived.__init__()
        Logger().info(f"Improper with: {self.base_data} and {self.improper_data}")


# Case 4: Serialization issues - DANGEROUS
def serialize_and_restore(obj: Base) -> Base:
    """Serialize and deserialize an object (can lose type information)."""
    Logger().info("Serializing and deserializing: ")
    serialized = pickle.dumps(obj)
    restored = pickle.loads(serialized)
    return restored


def run_demo() -> None:
    """Run the main demonstration."""
    Logger().info("Creating Derived object...")
    d = Derived()

    Logger().info("Original object:")
    d.print()
    Logger().info("")

    # Case 1: Python reference - works correctly
    process_by_reference(d)

    # Case 2: Copy - potential issues with shallow copying
    process_with_copy(d)

    # Case 3: Improper inheritance
    Logger().info("\nCreating ImproperInheritance object...")
    improper = ImproperInheritance()
    improper.print()  # Will be missing data that would be set in Derived.__init__

    # Case 4: Serialization
    Logger().info("\nTesting serialization:")
    restored = serialize_and_restore(d)
    # The object maintains its data but might not maintain all its methods
    restored.print()


if __name__ == "__main__":
    run_demo()
