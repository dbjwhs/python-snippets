"""
Visitor pattern implementation in Python.

This package implements the visitor design pattern for geometric shapes.
"""

from visitor_pattern.vistor import (
    AreaVisitor,
    Circle,
    DescriptionVisitor,
    PerimeterVisitor,
    Shape,
    ShapeVisitor,
    Square,
    Triangle,
)

__all__ = [
    "AreaVisitor",
    "Circle",
    "DescriptionVisitor",
    "PerimeterVisitor",
    "Shape",
    "ShapeVisitor",
    "Square",
    "Triangle",
]
