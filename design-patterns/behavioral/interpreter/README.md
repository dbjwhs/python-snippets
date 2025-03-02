# Python Interpreter Pattern Implementation

The Interpreter pattern is a behavioral design pattern that defines a grammatical representation for a language and provides an
interpreter to deal with this grammar. Originally introduced in the seminal "Design Patterns: Elements of Reusable Object-Oriented
Software" by the Gang of Four in 1994, this pattern emerged from the need to parse and evaluate domain-specific languages (DSLs) in a
structured and maintainable way.

This project implements the Interpreter pattern in Python using modern features like type hints, dataclasses, and abstract base classes.

## Installation and Setup

### Environment Setup

This project uses `uv` for package management. To set up a virtual environment and install the package:

```bash
# Navigate to the package directory
cd design-patterns/behavioral/interpreter

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in development mode with all development dependencies
uv pip install -e ".[dev]"
```

### Running Tests

Run the tests using pytest:

```bash
pytest
```

### Running Linter

Run the linter using ruff:

```bash
ruff check src tests examples
```

### Type Checking

Run type checking using mypy:

```bash
mypy src
```

## Usage

### Understanding the Launcher Scripts

This project provides two ways to run the interpreter pattern implementation and examples:

1. **Using the Python module syntax** (recommended for proper Python package practices)
   - This is the standard way to run a Python package
   - It ensures all imports work correctly with Python's package system
   - Example: `python -m interpreter_pattern`

2. **Using the convenience launcher scripts** (easier for quick execution)
   - These scripts handle the Python path setup automatically
   - They allow you to run the code without worrying about import paths
   - Useful if you run into import errors when trying to run the modules directly
   - Example: `python run_interpreter.py` or `./run_interpreter.py`

The launcher scripts solve common issues related to Python's import system when running scripts directly, making it easier to execute the code without setting up the Python path manually.

### Basic Usage

You can run the main example to see the interpreter pattern in action using either of these approaches:

Using the Python module syntax (recommended):
```bash
python -m interpreter_pattern
```

Or using the convenience launcher script:
```bash
# Add executable permission if needed
chmod +x run_interpreter.py

# Run directly
./run_interpreter.py

# Or using Python
python run_interpreter.py
```

### Calculator Example

A simple calculator example that demonstrates expression parsing and evaluation:

Using the Python module approach:
```bash
python examples/calculator_example.py
```

Or using the convenience launcher script:
```bash
# Add executable permission if needed
chmod +x run_calculator.py

# Run directly
./run_calculator.py

# Or using Python
python run_calculator.py
```

### Rule Engine Example

A more complex example that uses the interpreter pattern to build a business rule engine:

Using the Python module approach:
```bash
python examples/rule_engine_example.py
```

Or using the convenience launcher script:
```bash
# Add executable permission if needed
chmod +x run_rule_engine.py

# Run directly
./run_rule_engine.py

# Or using Python
python run_rule_engine.py
```

### Debugging Example with icecream

An example demonstrating how to use the icecream package for enhanced debugging:

Using the Python module approach:
```bash
python examples/debug_example.py
```

Or using the convenience launcher script:
```bash
# Add executable permission if needed
chmod +x run_debug.py

# Run directly
./run_debug.py

# Or using Python
python run_debug.py
```

## Core Components

### Expression

The Expression interface defines the core methods required for all expressions:

```python
from abc import ABC, abstractmethod
from interpreter_pattern.context import Context

class Expression(ABC):
    @abstractmethod
    def interpret(self, context: Context) -> int:
        pass
    
    @abstractmethod
    def to_string(self) -> str:
        pass
    
    def debug_print(self, depth: int = 0) -> None:
        # Prints debug information about the expression
        pass
```

### Context

The Context class stores variables and tracks operations during interpretation:

```python
from typing import Dict

class Context:
    def __init__(self) -> None:
        self._variables: Dict[str, int] = {}
        self._operation_count: int = 0
    
    def set_variable(self, name: str, value: int) -> None:
        # Set a variable value
        pass
    
    def get_variable(self, name: str) -> int:
        # Get a variable value
        pass
    
    def increment_operations(self) -> None:
        # Increment the operation counter
        pass
    
    def get_operation_count(self) -> int:
        # Get the current operation count
        pass
```

### Terminal Expressions

Terminal expressions represent simple values or variables:

```python
# Number literal expression
expr1 = NumberExpression(5)

# Variable reference expression
expr2 = VariableExpression("x")
```

### Non-terminal Expressions

Non-terminal expressions combine other expressions:

```python
# Addition expression
expr3 = AddExpression(expr1, expr2)

# Multiplication expression
expr4 = MultiplyExpression(NumberExpression(2), expr3)
```

### Evaluating Expressions

Expressions are evaluated within a context:

```python
# Create a context
context = Context()
context.set_variable("x", 10)

# Evaluate an expression
result = expr4.interpret(context)  # 2 * (5 + 10) = 30
```

## Examples

### Basic Arithmetic

```python
from interpreter_pattern.context import Context
from interpreter_pattern.expressions import (
    AddExpression, NumberExpression, MultiplyExpression
)

# Create expression: (5 + 3) * 2
expr = MultiplyExpression(
    AddExpression(
        NumberExpression(5),
        NumberExpression(3)
    ),
    NumberExpression(2)
)

context = Context()
result = expr.interpret(context)  # Result: 16
```

### Variables and Complex Expressions

```python
from interpreter_pattern.context import Context
from interpreter_pattern.expressions import (
    AddExpression, SubtractExpression, VariableExpression, 
    NumberExpression, MultiplyExpression
)

# Create context and set variables
context = Context()
context.set_variable("x", 10)
context.set_variable("y", 5)

# Create expression: (x + 2) * (y - 1)
expr = MultiplyExpression(
    AddExpression(
        VariableExpression("x"),
        NumberExpression(2)
    ),
    SubtractExpression(
        VariableExpression("y"),
        NumberExpression(1)
    )
)

result = expr.interpret(context)  # Result: (10 + 2) * (5 - 1) = 12 * 4 = 48
```

## License

This code is provided under the MIT License. Feel free to use, modify, and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.