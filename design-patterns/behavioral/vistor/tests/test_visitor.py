#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""Tests for the visitor pattern implementation."""

import math
from typing import cast

import pytest

from visitor_pattern.vistor import (
    AreaVisitor,
    Circle,
    DescriptionVisitor,
    PerimeterVisitor,
    Shape,
    Square,
    Triangle,
)


@pytest.fixture
def shapes() -> list[Shape]:
    """Create a list of shapes for testing."""
    return [
        Circle(radius=5.0),
        Square(side=4.0),
        Triangle(a=3.0, b=4.0, c=5.0),
    ]


@pytest.fixture
def area_visitor() -> AreaVisitor:
    """Create an area visitor for testing."""
    return AreaVisitor()


@pytest.fixture
def perimeter_visitor() -> PerimeterVisitor:
    """Create a perimeter visitor for testing."""
    return PerimeterVisitor()


@pytest.fixture
def description_visitor() -> DescriptionVisitor:
    """Create a description visitor for testing."""
    return DescriptionVisitor()


class TestShapes:
    """Tests for the Shape classes."""

    def test_circle_attributes(self) -> None:
        """Test Circle class attributes and methods."""
        circle = Circle(radius=5.0)
        assert circle.radius == 5.0
        assert circle.get_name() == "Circle"

    def test_square_attributes(self) -> None:
        """Test Square class attributes and methods."""
        square = Square(side=4.0)
        assert square.side == 4.0
        assert square.get_name() == "Square"

    def test_triangle_attributes(self) -> None:
        """Test Triangle class attributes and methods."""
        triangle = Triangle(a=3.0, b=4.0, c=5.0)
        assert triangle.a == 3.0
        assert triangle.b == 4.0
        assert triangle.c == 5.0
        assert triangle.get_name() == "Triangle"


class TestAreaVisitor:
    """Tests for the AreaVisitor class."""

    def test_circle_area(self, shapes: list[Shape], area_visitor: AreaVisitor) -> None:
        """Test area calculation for a circle."""
        circle = cast(Circle, shapes[0])
        expected_area = math.pi * circle.radius ** 2

        shapes[0].accept(area_visitor)
        assert math.isclose(area_visitor.get_area(), expected_area)

    def test_square_area(self, shapes: list[Shape], area_visitor: AreaVisitor) -> None:
        """Test area calculation for a square."""
        square = cast(Square, shapes[1])
        expected_area = square.side ** 2

        shapes[1].accept(area_visitor)
        assert math.isclose(area_visitor.get_area(), expected_area)

    def test_triangle_area(self, shapes: list[Shape], area_visitor: AreaVisitor) -> None:
        """Test area calculation for a triangle."""
        triangle = cast(Triangle, shapes[2])
        # 3-4-5 triangle has area 6
        expected_area = 6.0

        shapes[2].accept(area_visitor)
        assert math.isclose(area_visitor.get_area(), expected_area)

    def test_reset(self, shapes: list[Shape], area_visitor: AreaVisitor) -> None:
        """Test that the reset method clears the area value."""
        shapes[0].accept(area_visitor)
        assert area_visitor.get_area() > 0

        area_visitor.reset()
        assert area_visitor.get_area() == 0.0


class TestPerimeterVisitor:
    """Tests for the PerimeterVisitor class."""

    def test_circle_perimeter(self, shapes: list[Shape], perimeter_visitor: PerimeterVisitor) -> None:
        """Test perimeter calculation for a circle."""
        circle = cast(Circle, shapes[0])
        expected_perimeter = 2.0 * math.pi * circle.radius

        shapes[0].accept(perimeter_visitor)
        assert math.isclose(perimeter_visitor.get_perimeter(), expected_perimeter)

    def test_square_perimeter(self, shapes: list[Shape], perimeter_visitor: PerimeterVisitor) -> None:
        """Test perimeter calculation for a square."""
        square = cast(Square, shapes[1])
        expected_perimeter = 4.0 * square.side

        shapes[1].accept(perimeter_visitor)
        assert math.isclose(perimeter_visitor.get_perimeter(), expected_perimeter)

    def test_triangle_perimeter(
        self, shapes: list[Shape], perimeter_visitor: PerimeterVisitor
    ) -> None:
        """Test perimeter calculation for a triangle."""
        triangle = cast(Triangle, shapes[2])
        expected_perimeter = triangle.a + triangle.b + triangle.c

        shapes[2].accept(perimeter_visitor)
        assert math.isclose(perimeter_visitor.get_perimeter(), expected_perimeter)

    def test_reset(self, shapes: list[Shape], perimeter_visitor: PerimeterVisitor) -> None:
        """Test that the reset method clears the perimeter value."""
        shapes[0].accept(perimeter_visitor)
        assert perimeter_visitor.get_perimeter() > 0

        perimeter_visitor.reset()
        assert perimeter_visitor.get_perimeter() == 0.0


class TestDescriptionVisitor:
    """Tests for the DescriptionVisitor class."""

    def test_circle_description(
        self, shapes: list[Shape], description_visitor: DescriptionVisitor
    ) -> None:
        """Test description generation for a circle."""
        circle = cast(Circle, shapes[0])
        expected_description = f"A circle with radius {circle.radius}"

        shapes[0].accept(description_visitor)
        assert description_visitor.get_description() == expected_description

    def test_square_description(
        self, shapes: list[Shape], description_visitor: DescriptionVisitor
    ) -> None:
        """Test description generation for a square."""
        square = cast(Square, shapes[1])
        expected_description = f"A square with side length {square.side}"

        shapes[1].accept(description_visitor)
        assert description_visitor.get_description() == expected_description

    def test_triangle_description(
        self, shapes: list[Shape], description_visitor: DescriptionVisitor
    ) -> None:
        """Test description generation for a triangle."""
        triangle = cast(Triangle, shapes[2])
        expected_description = f"A triangle with sides {triangle.a}, {triangle.b}, and {triangle.c}"

        shapes[2].accept(description_visitor)
        assert description_visitor.get_description() == expected_description

    def test_reset(self, shapes: list[Shape], description_visitor: DescriptionVisitor) -> None:
        """Test that the reset method clears the description value."""
        shapes[0].accept(description_visitor)
        assert description_visitor.get_description() != ""

        description_visitor.reset()
        assert description_visitor.get_description() == ""
