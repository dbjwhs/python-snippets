# Negative Space Programming

Negative space programming is a coding philosophy that emerged from the intersection of visual arts principles, defensive programming, and
design by contract methodologies. Originally inspired by the artistic concept of negative space (the space around and between subjects)
from the early 1900s, this programming paradigm was formalized during the rise of robust software development practices in the 1970s and
1980s. The approach gained significant traction alongside the growth of defensive programming practices and Bertrand Meyer's [Design by
Contract (DbC)](https://en.wikipedia.org/wiki/Design_by_contract) methodology. Rather than defining what a program should do, negative space programming focuses on explicitly stating what
it should not do, creating clearer boundaries and more robust error handling through constraint-based design.

## Use Cases and Problem Solving

Negative space programming excels in scenarios where system boundaries and constraints are more important than specific behaviors. This
approach is particularly valuable in:

- Security-critical systems where defining forbidden states is crucial
- Data validation where invalid inputs must be explicitly rejected
- API design where clear constraints improve usability
- Resource management where preventing misuse is essential
- State machine implementations where invalid transitions must be prevented
- Configuration management where certain combinations must be forbidden

The pattern effectively addresses several common programming challenges:
- Unclear system boundaries
- Incomplete error handling
- Edge case oversight
- Implicit assumptions in code
- Brittle validation logic
- Security vulnerabilities from undefined behavior

## Implementation Examples

### Basic Constraint Example
```python
class SafeInteger:
    def __init__(self):
        self._value = 0
        self._forbidden_values = []
    
    def set_value(self, value: int) -> None:
        if value in self._forbidden_values:
            raise ValueError("forbidden value")
        self._value = value
```

### Advanced Application
```python
from typing import Generic, TypeVar, List, Callable, Any

T = TypeVar('T')

class NegativeSpaceContainer(Generic[T]):
    def __init__(self):
        self._data: List[T] = []
        self._constraints: List[Callable[[T], bool]] = []
    
    def add(self, item: T) -> None:
        for constraint in self._constraints:
            if constraint(item):
                raise ValueError("item violates constraints")
        self._data.append(item)
```

## Best Practices

### Do:
- Define explicit constraints first
- Document what is not allowed
- Use strong types to enforce constraints
- Implement comprehensive error handling
- Test boundary conditions extensively
- Make constraints configurable when appropriate

### Don't:
- Mix positive and negative space approaches unnecessarily
- Over-constrain your system
- Hide constraints in implementation details
- Ignore performance implications of constraint checking
- Forget to document constraint violations
- Make constraints too rigid for practical use

## Performance Considerations

Negative space programming can introduce additional overhead from:
- Constraint checking at runtime
- Additional validation logic
- Error handling overhead
- Memory usage for constraint storage

However, these costs are often justified by:
- Improved system reliability
- Better error detection
- Clearer system boundaries
- Reduced debugging time
- More maintainable code

## Related Design Patterns and Concepts

- Design by Contract (DbC)
- Defensive Programming
- Type-State Pattern
- Guard Clauses
- Fail-Fast Pattern
- Invariant Checking

## Further Reading

### Books
- "Design by Contract" by Bertrand Meyer
- "Code Complete" by Steve McConnell (Chapter on Defensive Programming)
- "Clean Code" by Robert C. Martin (Sections on Boundaries)

### Online Resources
- [Design by Contract Pattern](https://wiki.c2.com/?DesignByContract)
- [Defensive Programming Techniques](https://en.wikipedia.org/wiki/Defensive_programming)
- [Type-State Programming](https://en.wikipedia.org/wiki/Typestate_analysis)

## Setup and Usage

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with dev dependencies
uv pip install -e ".[dev]"

# Run the main example
python -m negative_space

# Run the advanced example
python -m negative_space.examples.advanced_example

# Or use the launcher scripts
./run_negative_space.py
./run_advanced_example.py

# Run tests
pytest

# Run linting
ruff check --fix .

# Run type checking
mypy .
```

## License
This code is provided under the MIT License. Feel free to use, modify, and distribute as needed.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.