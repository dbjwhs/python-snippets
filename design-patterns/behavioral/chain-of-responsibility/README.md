# Chain of Responsibility Design Pattern

The Chain of Responsibility is a behavioral design pattern that lets you pass requests along a chain of handlers. Upon receiving a request, each handler decides either to process the request or to pass it to the next handler in the chain. The pattern was first introduced by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides (known as the "Gang of Four") in their seminal 1994 book "Design Patterns: Elements of Reusable Object-Oriented Software". This pattern emerged from the need to decouple senders and receivers of requests, allowing multiple objects to handle the request without the sender needing to know which object will ultimately process it. The pattern promotes loose coupling and adheres to the Single Responsibility and Open/Closed principles of object-oriented design.

## Python Implementation

This repository contains a modern Python 3.10+ implementation of the Chain of Responsibility pattern, using type hints, generics, and dataclasses.

### Features
- Strongly typed using Python's type hints
- Uses abstract base classes to define the handler protocol
- Uses dataclasses for representing request objects
- Comprehensive test suite using pytest
- Example implementations for expense approval and document processing workflows

### Installation

To install this package using `uv`:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Getting Started

Here's a simple example of creating and using an expense approval chain:

```python
from chain_of_responsibility import (
    TeamLeader, 
    DepartmentManager, 
    Director, 
    CEO,
    ExpenseRequest
)

# Create the chain
team_leader = TeamLeader()
dept_manager = DepartmentManager()
director = Director()
ceo = CEO()

# Link the handlers
team_leader.set_next(dept_manager)
dept_manager.set_next(director)
director.set_next(ceo)

# Create and process a request
request = ExpenseRequest(12000.0, "new software licenses")
result = team_leader.process_request(request.amount, request.purpose)
print(f"Approval result: {'Approved' if result else 'Rejected'}")
```

## Use Cases and Problem Solving

The Chain of Responsibility pattern is particularly valuable in scenarios where:

1. Multiple objects may handle a request, and the handler isn't known a priori
2. You want to issue a request to one of several objects without explicitly specifying the receiver
3. The set of objects that can handle a request should be specified dynamically

Common applications include:
- GUI event handling systems (events bubbling up through component hierarchy)
- Logging frameworks with different severity levels
- Authentication and authorization systems
- Request processing in web applications (middleware)
- Document approval workflows
- Exception handling in programming languages

## Python Implementation Examples

### Basic Structure
```python
from typing import Optional, Protocol, Self

class Handler(Protocol):
    def set_next(self, handler: "Handler") -> "Handler":
        ...
    
    def handle_request(self, request: any) -> bool:
        ...
```

### Common Variations

1. **Abstract Base Class Approach**
```python
from abc import ABC, abstractmethod
from typing import Optional

class AbstractHandler(ABC):
    def __init__(self) -> None:
        self._next_handler: Optional["AbstractHandler"] = None
        
    def set_next(self, handler: "AbstractHandler") -> "AbstractHandler":
        self._next_handler = handler
        return handler
        
    @abstractmethod
    def handle_request(self, request: any) -> bool:
        pass
```

2. **Functional Approach with Decorators**
```python
from typing import Callable, Any, TypeVar

T = TypeVar('T')
Handler = Callable[[T], bool]

def chain_handlers(*handlers: Handler[T]) -> Handler[T]:
    def chained_handler(request: T) -> bool:
        for handler in handlers:
            if handler(request):
                return True
        return False
    return chained_handler
```

## Running the Examples

This package includes a few examples demonstrating the Chain of Responsibility pattern:

1. **Basic Expense Approval System**

```bash
python -m src.chain_of_responsibility
```

2. **Document Approval Workflow**

```bash
python examples/custom_chain_example.py
```

## Testing

To run the test suite:

```bash
pytest
```

For coverage report:

```bash
pytest --cov
```

## Best Practices

1. Design Considerations:
    - Keep handler interfaces simple and focused
    - Consider using abstract factories to create chains
    - Document the expected chain structure
    - Consider implementing fall-through behavior

2. Performance Considerations:
    - Keep chains reasonably short
    - Consider implementing shortcuts for common cases
    - Monitor chain length at runtime
    - Consider implementing chain optimization strategies

## Advantages and Disadvantages

### Advantages
- Decouples senders from receivers
- Promotes single responsibility principle
- Flexible and dynamic request handling
- Easy to add or remove responsibilities
- Follows open/closed principle

### Disadvantages
- No guarantee of request handling
- Potential for broken chains
- Can be hard to debug
- May impact performance with long chains
- Potential for circular references

## Python-Specific Implementation Notes

1. **Type Annotations**
   - Use `Protocol` or `ABC` to define handler interfaces
   - Use `Optional[Handler]` for the next handler reference
   - Consider using generics (`TypeVar`) for request types

2. **Python Idioms**
   - Consider using a class method to create prebuilt chains
   - Use dataclasses for request objects
   - Use properties and descriptors for handler behavior customization

3. **Testing Considerations**
   - Use `pytest.fixture` to create reusable chains
   - Use mocking to test handler interactions
   - Test edge cases like empty chains or circular references

## License
This implementation is provided under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please feel free to submit pull requests with improvements or bug fixes.