#!/usr/bin/env python3
"""Advanced examples of Python object copying pitfalls.

This module demonstrates more complex scenarios where object information
can be lost due to inheritance, copying, or serialization issues.
"""

import json
from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable

from icecream import ic


@runtime_checkable
class Printable(Protocol):
    """Protocol for objects that can be printed."""

    def print(self) -> None:
        """Print information about the object."""
        ...


class ComplexBase(ABC):
    """A more complex base class with a mix of data and behavior."""

    def __init__(self, name: str, value: int) -> None:
        """Initialize the complex base."""
        self.name = name
        self.value = value
        self._internal_state: dict[str, Any] = {"initialized": True}

    @abstractmethod
    def print(self) -> None:
        """Print information about the object."""
        pass

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "value": self.value,
            "_internal_state": self._internal_state,
            "type": self.__class__.__name__,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ComplexBase":
        """Create an instance from a dictionary."""
        # This method doesn't handle creating the correct subclass
        instance = cls(data["name"], data["value"])
        instance._internal_state = data["_internal_state"]
        return instance


class ComplexDerived(ComplexBase):
    """A derived class with additional data and behavior."""

    def __init__(self, name: str, value: int, extra_data: list[str]) -> None:
        """Initialize the complex derived class."""
        super().__init__(name, value)
        self.extra_data = extra_data
        self._internal_state["has_extra_data"] = True

    def print(self) -> None:
        """Print information about the derived object."""
        ic(f"ComplexDerived: {self.name}, {self.value}, {self.extra_data}")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = super().to_dict()
        data["extra_data"] = self.extra_data
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ComplexDerived":
        """Create a ComplexDerived instance from a dictionary."""
        return cls(data["name"], data["value"], data["extra_data"])


def json_serialize_deserialize(obj: ComplexBase) -> dict[str, Any]:
    """Demonstrate issues with JSON serialization."""
    # Convert to JSON
    json_data = json.dumps(obj.to_dict())

    # Deserialize from JSON
    data = json.loads(json_data)

    # Notice we don't reconstruct the proper object type here
    # This is a common issue with serialization
    return data


def proper_json_deserialize(data: dict[str, Any]) -> ComplexBase:
    """Properly deserialize JSON based on the type field."""
    type_name = data.get("type")

    if type_name == "ComplexDerived":
        return ComplexDerived.from_dict(data)
    else:
        # In a real application, you would have a registry of types
        raise ValueError(f"Unknown type: {type_name}")


def demonstrate_advanced_issues() -> None:
    """Demonstrate advanced issues with copying and serialization."""
    # Create a derived object
    derived = ComplexDerived("example", 42, ["extra1", "extra2"])

    ic("Original object:")
    derived.print()

    # Issue 1: JSON serialization without proper deserialization
    ic("\nIssue 1: JSON serialization without proper type reconstruction")
    json_data = json_serialize_deserialize(derived)
    ic(f"Deserialized data (lost type information): {json_data}")

    # Issue 2: Proper JSON deserialization
    ic("\nIssue 2: Proper JSON deserialization with type reconstruction")
    properly_deserialized = proper_json_deserialize(json_data)
    properly_deserialized.print()

    # Issue 3: Generic function that loses type information
    ic("\nIssue 3: Generic function that doesn't preserve type")

    def process_generically(obj: Printable) -> None:
        """Process an object generically via the Printable protocol."""
        # The static type information is lost, only the protocol behavior remains
        obj.print()

    process_generically(derived)

    # Issue 4: Type casting problems
    ic("\nIssue 4: Type casting problems")

    # Create a simple base that happens to have a print method
    class SimpleObject:
        """A simple object that happens to have a print method."""

        def print(self) -> None:
            """Print information."""
            ic("I'm just a simple object!")

    simple = SimpleObject()

    # This works at runtime due to duck typing and runtime_checkable Protocol
    # but it's not actually a ComplexBase
    if isinstance(simple, Printable):
        process_generically(simple)

    # This will raise a TypeError if uncommented
    # complex_as_derived = cast(ComplexDerived, simple)
    # complex_as_derived.extra_data.append("this will fail")


if __name__ == "__main__":
    demonstrate_advanced_issues()
