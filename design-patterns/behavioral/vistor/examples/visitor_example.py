#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Example usage of the visitor pattern.

This script demonstrates how to use the visitor pattern to perform
various operations on geometric shapes.
"""

import os
import sys

# Add the parent directory to the path so we can import the visitor_pattern package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from icecream import ic

from visitor_pattern import (
    AreaVisitor,
    Circle,
    DescriptionVisitor,
    PerimeterVisitor,
    Shape,
    Square,
    Triangle,
)


def main() -> None:
    """Example usage of the visitor pattern with custom shapes."""
    ic("Visitor Pattern Example")

    # Create some shapes
    shapes: list[Shape] = [
        Circle(radius=10.0),
        Square(side=7.5),
        Triangle(a=5.0, b=7.0, c=9.0),
    ]

    # Create visitors
    area_visitor = AreaVisitor()
    perimeter_visitor = PerimeterVisitor()
    description_visitor = DescriptionVisitor()

    # Process each shape with all visitors
    ic("Processing shapes with visitors:")

    for shape in shapes:
        ic(f"Shape: {shape.get_name()}")

        # Calculate area
        shape.accept(area_visitor)
        ic(f"  Area: {area_visitor.get_area():.2f}")

        # Calculate perimeter
        shape.accept(perimeter_visitor)
        ic(f"  Perimeter: {perimeter_visitor.get_perimeter():.2f}")

        # Generate description
        shape.accept(description_visitor)
        ic(f"  Description: {description_visitor.get_description()}")

        # Reset visitors for next shape
        area_visitor.reset()
        perimeter_visitor.reset()
        description_visitor.reset()

        ic("---")

    ic("Example completed successfully")


if __name__ == "__main__":
    main()
