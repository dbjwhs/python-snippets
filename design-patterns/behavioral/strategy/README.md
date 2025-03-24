# Strategy Pattern

The Strategy Pattern is a behavioral design pattern that was introduced by the "Gang of Four" (Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides) in their seminal 1994 book "Design Patterns: Elements of Reusable Object-Oriented Software". This pattern enables defining a family of algorithms, encapsulating each one, and making them interchangeable. It lets the algorithm vary independently from clients that use it. The pattern emerged from the need to provide a way to configure a class with one of many behaviors, and to provide a way to change or extend those behaviors without altering the class itself. This aligns perfectly with the Open/Closed Principle, one of the fundamental principles of object-oriented design.

## Use Cases & Problem Solutions

The Strategy Pattern effectively solves several common software design challenges:

1. When you need to use different variants of an algorithm within an object and be able to switch from one algorithm to another during runtime
2. When you have a lot of similar classes that only differ in the way they execute some behavior
3. When you need to isolate the algorithm implementation details from the code that uses the algorithm
4. When a class defines many behaviors, and these appear as multiple conditional statements in its operations

Common real-world applications include:
- Payment processing systems with multiple payment methods
- Compression algorithms where different compression methods can be used
- Navigation systems that can use different routing algorithms
- Sorting mechanisms where different sorting algorithms can be applied based on data characteristics
- Authentication strategies in security systems

## Implementation Examples & Best Practices

### Good Implementation Characteristics

1. Clean Interface Segregation:
```python
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass
        
    @property
    @abstractmethod
    def payment_method(self) -> str:
        pass
```

2. Context Class Independence:
```python
class ShoppingCart:
    def __init__(self) -> None:
        self._payment_strategy: Optional[PaymentStrategy] = None
        
    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        self._payment_strategy = strategy
```

### Anti-patterns to Avoid

1. Tight Coupling:
```python
# Bad: Hard-coded strategy selection
if payment_type == "CREDIT":
    process_credit_card()
elif payment_type == "PAYPAL":
    process_paypal()
```

2. Strategy Bloat:
```python
# Bad: Too many responsibilities in strategy
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass
        
    @abstractmethod
    def validate_user(self) -> bool:  # Should be separate concern
        pass
        
    @abstractmethod
    def generate_report(self) -> str:  # Should be separate concern
        pass
```

## When Not to Use

The Strategy Pattern might be overkill in these situations:
- When you have a fixed set of algorithms that rarely changes
- When the algorithms are simple and the overhead of creating new classes isn't justified
- When the context class is simple and doesn't need to switch between different algorithms

## Notable Books & Resources

1. "Design Patterns: Elements of Reusable Object-Oriented Software" (1994)
    - Original source of the pattern
    - Provides comprehensive theoretical foundation

2. "Head First Design Patterns" by Eric Freeman & Elisabeth Robson
    - Offers practical examples and visual explanations
    - Great for beginners

3. "Refactoring to Patterns" by Joshua Kerievsky
    - Shows how to evolve towards using the Strategy Pattern
    - Real-world refactoring examples

4. "Pattern-Oriented Software Architecture" by Buschmann, Meunier, Rohnert, Sommerlad, and Stal
    - Covers architectural implications
    - Advanced pattern relationships

## Pattern Variations

1. Static Strategy: Where the strategy is set at compile-time using generics
```python
from typing import Generic, TypeVar

T = TypeVar('T', bound='Strategy')

class Context(Generic[T]):
    def __init__(self, strategy: T) -> None:
        self.strategy = strategy
        
    def execute_strategy(self) -> None:
        self.strategy.execute()
```

2. Function-based Strategy: Using callable for lightweight strategy implementation
```python
from typing import Callable

class Context:
    def __init__(self) -> None:
        self.strategy: Callable[[int], None] = lambda x: None
        
    def set_strategy(self, new_strategy: Callable[[int], None]) -> None:
        self.strategy = new_strategy
```

## Related Patterns

- State Pattern: Similar structure but different intent. State pattern allows an object to alter its behavior when its internal state changes.
- Command Pattern: Can use Strategy as part of its implementation.
- Template Method: Defines algorithm skeleton in base class but lets subclasses override specific steps.

## Key Benefits

1. Flexibility: Easy to add new strategies without changing existing code
2. Reusability: Strategies can be shared across different contexts
3. Testability: Each strategy can be tested in isolation
4. Maintainability: Changes to one strategy don't affect others
5. Runtime Behavior Change: Allows for dynamic algorithm selection

Remember that the Strategy Pattern is most effective when:
- The algorithmic variation is significant
- The algorithms need to be interchangeable
- The algorithm selection needs to happen at runtime
- The algorithms can be cleanly encapsulated

## Setup and Usage

### Installation

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
.venv\Scripts\activate     # On Windows

# Install the package in development mode
uv pip install -e ".[dev]"
```

### Running the Example

```bash
# Run the payment example
python examples/payment_example.py

# Or run the package directly
python -m strategy_pattern
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=strategy_pattern
```

### Linting and Type Checking

```bash
# Run ruff linter
ruff check .

# Run mypy type checker
mypy src/
```

## License

This code is provided under the MIT License. Feel free to use, modify, and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.