# python-snippets
A mono repo to contain my personal snippets for Python, with most my endeavor to port my C++ snippets to Python.

## Design Patterns

### Behavioral Patterns

#### [Command Pattern](design-patterns/behavioral/command/)
A Python implementation of the Command design pattern, ported from C++. Turns requests into stand-alone objects that contain all information about the request. Includes document editing system and smart home automation examples with undo/redo functionality.

##### Setup and Usage
```bash
cd design-patterns/behavioral/command/command_pattern
uv venv
. .venv/bin/activate
uv pip install -e ".[dev]"

# Run the main example
python -m command_pattern

# Run specific examples
python -m command_pattern.examples.document_example
python -m command_pattern.examples.smart_home_example

# Run tests
pytest

# Run linting
ruff check .
```

#### [Chain of Responsibility](design-patterns/behavioral/chain-of-responsibility/)
A Python implementation of the Chain of Responsibility design pattern, ported from C++. Uses modern Python features like type hints, dataclasses, and abstract base classes. Includes an expense approval system example and a document workflow example.

##### Setup and Usage
```bash
cd design-patterns/behavioral/chain-of-responsibility
uv venv
. .venv/bin/activate
uv pip install -e .

# Run the main example
python -m src.chain_of_responsibility

# Run the document approval example
python examples/custom_chain_example.py

# Run tests
pytest
```

#### [Fail-Fast Pattern](design-patterns/behavioral/fail-fast/)
A Python implementation of the Fail-Fast pattern, ported from C++. Uses modern Python with type hints and proper error handling. Demonstrates immediate error detection through state validation and early exception raising. Includes a banking system implementation with comprehensive validation.

##### Setup and Usage
```bash
cd design-patterns/behavioral/fail-fast
uv venv
. .venv/bin/activate
uv pip install -e ".[dev]"

# Run the main example
python -m fail_fast

# Run the banking example
python examples/banking_example.py

# Run tests
pytest

# Run type checking 
mypy src

# Run linting
ruff check src tests examples
```

## Data Structures

### [Binary Tree](data-structures/binary-tree/)
A Python implementation of a binary search tree that works with any comparable type. Includes in-order, pre-order, and post-order traversals.

#### Setup and Usage
```bash
cd data-structures/binary-tree
uv venv
. .venv/bin/activate
uv pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
```
