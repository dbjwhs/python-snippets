# Abstract Factory Design Pattern

The Abstract Factory pattern, introduced in 1994 by the "Gang of Four" (GoF) in their seminal work "Design Patterns: Elements of Reusable Object-Oriented Software," is a creational design pattern that provides an interface for creating families of related or dependent objects without specifying their concrete classes. This pattern emerged from the need to handle platform independence in object-oriented systems, particularly in GUI frameworks where different operating systems required different widget implementations. The pattern's origins can be traced back to earlier systems like InterViews and ET++ that needed to manage cross-platform compatibility while maintaining consistent object families.

## Problem & Solution Space

The Abstract Factory pattern addresses several critical challenges in software design:

1. **Platform Independence**: Enables applications to work with multiple platforms or systems by encapsulating platform-specific object creation.
2. **Product Family Consistency**: Ensures that created objects work together harmoniously by guaranteeing they come from the same family or theme.
3. **Configuration Flexibility**: Allows systems to be configured with different product families at runtime without modifying client code.
4. **Dependency Management**: Helps maintain loose coupling between concrete products and client code by working with abstractions.

## Common Use Cases

- **GUI Libraries**: Creating consistent widget sets across different operating systems
- **Database Access**: Managing different database connectors and their related components
- **Theme Systems**: Implementing consistent theming across application components
- **Document Creation**: Generating different document formats (PDF, HTML, etc.) with consistent styling
- **Game Development**: Creating different character types with consistent attributes for different game levels or environments

## Implementation Guide

### Basic Structure
```python
class AbstractFactory(ABC):
    @abstractmethod
    def create_product_a(self) -> ProductA:
        pass
        
    @abstractmethod
    def create_product_b(self) -> ProductB:
        pass
```

### Key Components
1. Abstract Factory Interface
2. Concrete Factories
3. Abstract Products
4. Concrete Products

## Advantages

- Promotes consistency among product families
- Supports the Open/Closed Principle
- Makes product swapping trivial
- Centralizes product creation logic
- Facilitates testing through abstraction

## Disadvantages

- It can be overkill for simple creation scenarios
- Adding new product types requires modifying all factory classes
- It can lead to a proliferation of interfaces and classes
- It may introduce unnecessary complexity for small product families

## Best Practices

1. **Factory Method Combination**: Often used in conjunction with Factory Method pattern for flexible object creation
2. **Singleton Usage**: Abstract Factories are frequently implemented as singletons
3. **Interface Segregation**: Consider splitting large factory interfaces into smaller, more focused ones
4. **Dependency Injection**: Use DI containers to manage factory instances
5. **Configuration Management**: Implement factory selection based on configuration files or environment variables

## Real-World Examples

### Cross-Platform GUI Framework
```python
class Button(Protocol):
    def render(self) -> None: ...

class Window(Protocol):
    def display(self) -> None: ...

class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
        
    @abstractmethod
    def create_window(self) -> Window:
        pass

class WindowsFactory(GUIFactory):
    # Implementation for Windows
    ...

class MacFactory(GUIFactory):
    # Implementation for Mac
    ...
```

### Database Connection System
```python
class Connection(Protocol):
    def connect(self) -> bool: ...

class Command(Protocol):
    def execute(self, query: str) -> Any: ...

class DBFactory(ABC):
    @abstractmethod
    def create_connection(self) -> Connection:
        pass
        
    @abstractmethod
    def create_command(self) -> Command:
        pass

class MySQLFactory(DBFactory):
    # Implementation for MySQL
    ...

class PostgreSQLFactory(DBFactory):
    # Implementation for PostgreSQL
    ...
```

## Getting Started with This Project

### Requirements
- Python 3.12 or higher
- uv (package manager)

### Installation

1. Clone the repository
2. Create a virtual environment and install dependencies:

```bash
# Create and activate virtual environment with uv
uv venv
source .venv/bin/activate  # On Unix/Linux
# OR
.venv\Scripts\activate  # On Windows

# Install dependencies
uv pip install -e ".[dev]"
```

### Running the Examples

You can run the examples using one of the following methods:

1. Using the launcher scripts (recommended):
```bash
# Run the abstract factory demo
./run_abstract_factory.py

# Run the theme switcher example
./run_example.py
```

2. As a Python module:
```bash
python -m abstract_factory
```

3. From the source directory:
```bash
cd src
python -m abstract_factory.abstract_factory
```

### Running Tests

```bash
pytest
```

## Further Reading

### Books
1. "Design Patterns: Elements of Reusable Object-Oriented Software" by Gamma, Helm, Johnson, Vlissides
2. "Head First Design Patterns" by Freeman & Freeman
3. "Patterns of Enterprise Application Architecture" by Martin Fowler
4. "Clean Architecture" by Robert C. Martin
5. "Fluent Python" by Luciano Ramalho

### Online Resources
- [RefactoringGuru's Abstract Factory Pattern](https://refactoring.guru/design-patterns/abstract-factory)
- [SourceMaking's Abstract Factory Pattern](https://sourcemaking.com/design_patterns/abstract_factory)
- [Real Python's Design Patterns in Python](https://realpython.com/factory-method-python/)

## Related Patterns

- Factory Method
- Builder
- Prototype
- Singleton
- Dependency Injection

## Historical Context

The Abstract Factory pattern has evolved significantly since its introduction. Early implementations focused primarily on GUI widgets, but modern applications have expanded its use to various domains. The pattern has adapted to modern programming paradigms, incorporating concepts like:

- Type hints and protocols for better type safety
- Dataclasses for cleaner product implementations
- Dependency injection frameworks
- Modern Python features (type checking, protocols, structural typing)

## Common Pitfalls

1. **Over-abstraction**: Creating unnecessary abstraction layers when simple factory methods would suffice
2. **Rigid Hierarchies**: Making factories too specific, limiting their reusability
3. **Performance Overhead**: Adding unnecessary direction in performance-critical code
4. **Maintenance Burden**: Creating too many parallel hierarchies that become difficult to maintain
5. **Interface Bloat**: Adding too many product types to a single factory interface