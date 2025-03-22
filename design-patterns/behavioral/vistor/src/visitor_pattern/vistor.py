#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Visitor design pattern implementation in Python.

History and overview:
The visitor pattern is a behavioral design pattern that was first described in the "Gang of Four" (GoF) book
"Design Patterns: Elements of Reusable Object-Oriented Software" published in 1994 by Erich Gamma, Richard Helm,
Ralph Johnson, and John Vlissides. It allows adding new operations to existing object structures without modifying them.

How it works:
- Defines a separate visitor object that encapsulates an operation to be performed on elements of an object structure
- Allows defining new operations without changing the classes of the elements on which they operate
- Implements double dispatch, meaning the operation executed depends on both the type of visitor and the type of element

Common usages:
1. When a complex object structure contains many different object types with differing interfaces
2. When new operations need to be added frequently to the object structure without changing its classes
3. When operations on the object structure need to be decoupled from the structure itself
4. When applying operations across a diverse set of unrelated classes
5. In compilers (for traversing abstract syntax trees)
6. In document object models (for traversing and operating on XML/HTML elements)

Advantages:
- Open/closed principle: adds new operations without modifying existing classes
- Single responsibility principle: separates algorithms from the objects they operate on
- Collects related operations in one class and separates unrelated ones

Disadvantages:
- Breaks encapsulation as visitors must access element internals
- Difficult to add new element types as it requires updating all visitors
- Can lead to a complex design if overused
"""

import abc
import math
from dataclasses import dataclass, field
from typing import Protocol

from icecream import ic


class ShapeVisitor(Protocol):
    """
    Visitor interface that defines visit methods for each concrete element type.
    
    This protocol defines the interface for all visitors. Each visitor must implement
    visit methods for all supported shape types.
    """

    def visit_circle(self, circle: "Circle") -> None:
        """Visit a Circle element."""
        ...

    def visit_square(self, square: "Square") -> None:
        """Visit a Square element."""
        ...

    def visit_triangle(self, triangle: "Triangle") -> None:
        """Visit a Triangle element."""
        ...


class Shape(abc.ABC):
    """
    Abstract base class for all shapes.
    
    This class defines the common interface for all shapes in the visitor pattern.
    All concrete shapes must implement the accept and get_name methods.
    """

    @abc.abstractmethod
    def accept(self, visitor: ShapeVisitor) -> None:
        """
        Accept a visitor to perform operations on this shape.
        
        Args:
            visitor: The visitor object that will operate on this shape
        """
        pass

    @abc.abstractmethod
    def get_name(self) -> str:
        """
        Get the name of this shape.
        
        Returns:
            The name of the shape as a string
        """
        pass


@dataclass
class Circle(Shape):
    """
    Concrete Circle shape implementation.
    
    Attributes:
        radius: The radius of the circle
    """

    radius: float

    def accept(self, visitor: ShapeVisitor) -> None:
        """Accept a visitor by calling its visit_circle method."""
        visitor.visit_circle(self)

    def get_name(self) -> str:
        """Get the name of this shape."""
        return "Circle"


@dataclass
class Square(Shape):
    """
    Concrete Square shape implementation.
    
    Attributes:
        side: The side length of the square
    """

    side: float

    def accept(self, visitor: ShapeVisitor) -> None:
        """Accept a visitor by calling its visit_square method."""
        visitor.visit_square(self)

    def get_name(self) -> str:
        """Get the name of this shape."""
        return "Square"


@dataclass
class Triangle(Shape):
    """
    Concrete Triangle shape implementation.
    
    Attributes:
        a: Length of first side
        b: Length of second side
        c: Length of third side
    """

    a: float
    b: float
    c: float

    def accept(self, visitor: ShapeVisitor) -> None:
        """Accept a visitor by calling its visit_triangle method."""
        visitor.visit_triangle(self)

    def get_name(self) -> str:
        """Get the name of this shape."""
        return "Triangle"


@dataclass
class AreaVisitor:
    """
    Concrete visitor that calculates the area of shapes.
    
    Attributes:
        area: The calculated area value, initialized to 0.0
    """

    area: float = field(default=0.0)

    def reset(self) -> None:
        """Reset the area value to 0."""
        self.area = 0.0

    def get_area(self) -> float:
        """Get the calculated area value."""
        return self.area

    def visit_circle(self, circle: Circle) -> None:
        """
        Calculate and store the area of a circle.
        
        Args:
            circle: The circle to calculate the area for
        """
        self.area = math.pi * circle.radius ** 2
        ic(f"Calculated area of {circle.get_name()} with radius {circle.radius}: {self.area}")

    def visit_square(self, square: Square) -> None:
        """
        Calculate and store the area of a square.
        
        Args:
            square: The square to calculate the area for
        """
        self.area = square.side ** 2
        ic(f"Calculated area of {square.get_name()} with side {square.side}: {self.area}")

    def visit_triangle(self, triangle: Triangle) -> None:
        """
        Calculate and store the area of a triangle using Heron's formula.
        
        Heron's formula calculates the area of a triangle when the lengths of all 
        three sides are known, without needing to calculate the height or angles.
        
        Args:
            triangle: The triangle to calculate the area for
        """
        # Calculate semi-perimeter
        semi_perimeter = (triangle.a + triangle.b + triangle.c) / 2.0

        # Calculate area using Heron's formula
        self.area = math.sqrt(
            semi_perimeter
            * (semi_perimeter - triangle.a)
            * (semi_perimeter - triangle.b)
            * (semi_perimeter - triangle.c)
        )

        ic(f"Calculated area of {triangle.get_name()} with sides {triangle.a}, "
           f"{triangle.b}, {triangle.c}: {self.area}")


@dataclass
class PerimeterVisitor:
    """
    Concrete visitor that calculates the perimeter of shapes.
    
    Attributes:
        perimeter: The calculated perimeter value, initialized to 0.0
    """

    perimeter: float = field(default=0.0)

    def reset(self) -> None:
        """Reset the perimeter value to 0."""
        self.perimeter = 0.0

    def get_perimeter(self) -> float:
        """Get the calculated perimeter value."""
        return self.perimeter

    def visit_circle(self, circle: Circle) -> None:
        """
        Calculate and store the perimeter (circumference) of a circle.
        
        Args:
            circle: The circle to calculate the perimeter for
        """
        self.perimeter = 2.0 * math.pi * circle.radius
        ic(f"Calculated perimeter of {circle.get_name()} with radius {circle.radius}: {self.perimeter}")

    def visit_square(self, square: Square) -> None:
        """
        Calculate and store the perimeter of a square.
        
        Args:
            square: The square to calculate the perimeter for
        """
        self.perimeter = 4.0 * square.side
        ic(f"Calculated perimeter of {square.get_name()} with side {square.side}: {self.perimeter}")

    def visit_triangle(self, triangle: Triangle) -> None:
        """
        Calculate and store the perimeter of a triangle.
        
        Args:
            triangle: The triangle to calculate the perimeter for
        """
        self.perimeter = triangle.a + triangle.b + triangle.c
        ic(f"Calculated perimeter of {triangle.get_name()} with sides {triangle.a}, "
           f"{triangle.b}, {triangle.c}: {self.perimeter}")


@dataclass
class DescriptionVisitor:
    """
    Concrete visitor that generates text descriptions of shapes.
    
    Attributes:
        description: The generated description string, initialized to empty string
    """

    description: str = field(default="")

    def reset(self) -> None:
        """Reset the description to an empty string."""
        self.description = ""

    def get_description(self) -> str:
        """Get the generated description."""
        return self.description

    def visit_circle(self, circle: Circle) -> None:
        """
        Generate and store a description for a circle.
        
        Args:
            circle: The circle to describe
        """
        self.description = f"A circle with radius {circle.radius}"
        ic(f"Generated description: {self.description}")

    def visit_square(self, square: Square) -> None:
        """
        Generate and store a description for a square.
        
        Args:
            square: The square to describe
        """
        self.description = f"A square with side length {square.side}"
        ic(f"Generated description: {self.description}")

    def visit_triangle(self, triangle: Triangle) -> None:
        """
        Generate and store a description for a triangle.
        
        Args:
            triangle: The triangle to describe
        """
        self.description = f"A triangle with sides {triangle.a}, {triangle.b}, and {triangle.c}"
        ic(f"Generated description: {self.description}")


def main() -> None:
    """
    Main function that demonstrates the visitor pattern with shape examples.
    """
    ic("Starting Visitor Pattern Example")

    # Create shapes
    shapes: list[Shape] = [
        Circle(radius=5.0),
        Square(side=4.0),
        Triangle(a=3.0, b=4.0, c=5.0)
    ]

    ic(f"Created {len(shapes)} shapes for testing")

    # Create visitors
    area_visitor = AreaVisitor()
    perimeter_visitor = PerimeterVisitor()
    description_visitor = DescriptionVisitor()

    ic("Created visitors: AreaVisitor, PerimeterVisitor, DescriptionVisitor")

    # Test area calculations
    ic("Testing area calculations...")

    # Expected values for testing
    expected_circle_area = math.pi * 5.0 * 5.0
    expected_square_area = 4.0 * 4.0
    expected_triangle_area = 6.0  # 3-4-5 triangle has area 6

    # Test circle area
    shapes[0].accept(area_visitor)
    circle_area = area_visitor.get_area()
    ic(f"Circle area: {circle_area}, Expected: {expected_circle_area}")
    assert abs(circle_area - expected_circle_area) < 0.0001

    # Test square area
    shapes[1].accept(area_visitor)
    square_area = area_visitor.get_area()
    ic(f"Square area: {square_area}, Expected: {expected_square_area}")
    assert abs(square_area - expected_square_area) < 0.0001

    # Test triangle area
    shapes[2].accept(area_visitor)
    triangle_area = area_visitor.get_area()
    ic(f"Triangle area: {triangle_area}, Expected: {expected_triangle_area}")
    assert abs(triangle_area - expected_triangle_area) < 0.0001

    # Test perimeter calculations
    ic("Testing perimeter calculations...")

    # Expected values for testing
    expected_circle_perimeter = 2.0 * math.pi * 5.0
    expected_square_perimeter = 4.0 * 4.0
    expected_triangle_perimeter = 3.0 + 4.0 + 5.0

    # Test circle perimeter
    shapes[0].accept(perimeter_visitor)
    circle_perimeter = perimeter_visitor.get_perimeter()
    ic(f"Circle perimeter: {circle_perimeter}, Expected: {expected_circle_perimeter}")
    assert abs(circle_perimeter - expected_circle_perimeter) < 0.0001

    # Test square perimeter
    shapes[1].accept(perimeter_visitor)
    square_perimeter = perimeter_visitor.get_perimeter()
    ic(f"Square perimeter: {square_perimeter}, Expected: {expected_square_perimeter}")
    assert abs(square_perimeter - expected_square_perimeter) < 0.0001

    # Test triangle perimeter
    shapes[2].accept(perimeter_visitor)
    triangle_perimeter = perimeter_visitor.get_perimeter()
    ic(f"Triangle perimeter: {triangle_perimeter}, Expected: {expected_triangle_perimeter}")
    assert abs(triangle_perimeter - expected_triangle_perimeter) < 0.0001

    # Test description generation
    ic("Testing description generation...")

    # Expected descriptions
    expected_circle_desc = "A circle with radius 5.0"
    expected_square_desc = "A square with side length 4.0"
    expected_triangle_desc = "A triangle with sides 3.0, 4.0, and 5.0"

    # Test circle description
    shapes[0].accept(description_visitor)
    circle_desc = description_visitor.get_description()
    ic(f"Circle description: {circle_desc}")
    assert circle_desc == expected_circle_desc

    # Test square description
    shapes[1].accept(description_visitor)
    square_desc = description_visitor.get_description()
    ic(f"Square description: {square_desc}")
    assert square_desc == expected_square_desc

    # Test triangle description
    shapes[2].accept(description_visitor)
    triangle_desc = description_visitor.get_description()
    ic(f"Triangle description: {triangle_desc}")
    assert triangle_desc == expected_triangle_desc

    # Demonstrate polymorphic behavior through a shape collection
    ic("Demonstrating polymorphic behavior through shape collection...")

    # Iterate through all shapes and apply all visitors
    for shape in shapes:
        ic(f"Processing shape: {shape.get_name()}")

        # Reset visitors
        area_visitor.reset()
        perimeter_visitor.reset()
        description_visitor.reset()

        # Apply all visitors to current shape
        shape.accept(area_visitor)
        shape.accept(perimeter_visitor)
        shape.accept(description_visitor)

        # Log results
        ic(f"Results for {shape.get_name()}: Area = {area_visitor.get_area()}, "
           f"Perimeter = {perimeter_visitor.get_perimeter()}, "
           f"Description = '{description_visitor.get_description()}'")

    ic("All tests passed successfully!")


if __name__ == "__main__":
    main()
