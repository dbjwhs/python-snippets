# Visitor Design Pattern Implementation in Python

The Visitor pattern is a behavioral design pattern that allows you to separate algorithms from the objects on which they
operate. It was first introduced in the influential "Gang of Four" book (Design Patterns: Elements of Reusable
Object-Oriented Software) by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, published in 1994. The pattern
enables adding new operations to existing object structures without modifying those structures. It represents a way to
implement "double dispatch" in languages like Python that don't natively support it, meaning the operation performed depends
on both the type of the visitor and the type of the element being visited.

## Use Cases and Problem Solutions

The Visitor pattern is particularly useful when you have a stable hierarchy of classes and need to perform various
operations on them that don't belong in the class hierarchy itself. It addresses several common problems in
object-oriented design: how to add functionality to a class hierarchy without changing it, how to keep related operations
together, and how to perform operations that span multiple unrelated classes. This pattern is ideal when you want to
perform operations across a disparate set of objects with different interfaces, enabling these operations to be changed
independently of the objects they work on. Use cases include compilers (for traversing abstract syntax trees), document
object models (for XML/HTML processing), and complex report generation systems.

## Installation

### Using uv (recommended)

```bash
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Verify Installation

```bash
python -m visitor_pattern
```

## Core Components

### Visitor Interface
```python
class ShapeVisitor(Protocol):
    def visit_circle(self, circle: Circle) -> None:
        """Visit a Circle element."""
        ...
    
    def visit_square(self, square: Square) -> None:
        """Visit a Square element."""
        ...
    
    def visit_triangle(self, triangle: Triangle) -> None:
        """Visit a Triangle element."""
        ...
```

### Element Interface
```python
class Shape(abc.ABC):
    @abc.abstractmethod
    def accept(self, visitor: ShapeVisitor) -> None:
        """Accept a visitor to perform operations on this shape."""
        pass
    
    @abc.abstractmethod
    def get_name(self) -> str:
        """Get the name of this shape."""
        pass
```

### Concrete Elements
```python
@dataclass
class Circle(Shape):
    radius: float
    
    def accept(self, visitor: ShapeVisitor) -> None:
        visitor.visit_circle(self)
    
    def get_name(self) -> str:
        return "Circle"

# Similarly for Square and Triangle
```

### Concrete Visitors
```python
@dataclass
class AreaVisitor:
    area: float = field(default=0.0)
    
    def visit_circle(self, circle: Circle) -> None:
        self.area = math.pi * circle.radius ** 2
        
    # Methods for other shapes...

# Similarly for PerimeterVisitor and DescriptionVisitor
```

## Implementation Details

This implementation showcases a geometric shape processing system. It includes:
- A shape hierarchy (Circle, Square, Triangle)
- Multiple visitors (AreaVisitor, PerimeterVisitor, DescriptionVisitor)
- Comprehensive testing with pytest

## Heron's Formula for Triangle Area

In the AreaVisitor, we use Heron's formula to calculate the area of a triangle. Named after Heron of Alexandria, this
formula calculates the area of a triangle when the lengths of all three sides are known, without needing to calculate the
height or angles.

The formula states:
```
Area = √(s(s-a)(s-b)(s-c))
```

Where:
- a, b, c are the lengths of the sides of the triangle
- s is the semi-perimeter: s = (a + b + c)/2

This elegant formula works for any triangle and is particularly useful in the Visitor pattern context as it allows us to
compute the area using only the properties exposed by the Triangle class, demonstrating how visitors can perform complex
calculations specific to each element type.

## Running the Examples

There are multiple ways to run the examples:

### Using the Python Module

```bash
python -m visitor_pattern
```

### Using the Launcher Scripts

```bash
# Run the main visitor demo
./run_visitor.py

# Run the extended example
./run_example.py
```

### Running Tests

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=visitor_pattern
```

## Usage Example

```python
from visitor_pattern import (
    Circle, Square, Shape, 
    AreaVisitor, PerimeterVisitor
)

# Create shapes
circle = Circle(radius=5.0)
square = Square(side=4.0)

# Create visitors
area_visitor = AreaVisitor()
perimeter_visitor = PerimeterVisitor()

# Apply visitors to shapes
circle.accept(area_visitor)
square.accept(perimeter_visitor)

# Get results
circle_area = area_visitor.get_area()
square_perimeter = perimeter_visitor.get_perimeter()

print(f"Circle area: {circle_area}")
print(f"Square perimeter: {square_perimeter}")
```

## Advantages

1. **Open/Closed Principle**: New operations can be added without modifying the element classes
2. **Single Responsibility Principle**: Each visitor encapsulates a specific algorithm or operation
3. **Consolidation of Related Operations**: Related behaviors are kept together in visitor classes
4. **Type Safety**: The pattern provides type-safe operations across heterogeneous object collections

## Disadvantages

1. **Breaks Encapsulation**: Visitors may need access to the internal details of elements
2. **Rigidity in Element Hierarchy**: Adding new element types requires updating all visitor interfaces
3. **Complexity**: Can lead to complex designs if overused
4. **Runtime Overhead**: Double dispatch mechanism adds some overhead

## Related Patterns

- **Composite Pattern**: Visitor is often used with Composite to operate on complex object structures
- **Iterator Pattern**: Visitors commonly use Iterators to traverse object structures
- **Command Pattern**: Both separate operations from objects, but in different ways

## Further Reading

1. "Design Patterns: Elements of Reusable Object-Oriented Software" by Gamma, Helm, Johnson, Vlissides
2. "Python Design Patterns" by Brandon Rhodes
3. "Fluent Python" by Luciano Ramalho

## License

This code is provided under the MIT License. Feel free to use, modify, and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.