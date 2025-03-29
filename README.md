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

#### [Interpreter Pattern](design-patterns/behavioral/interpreter/)
A Python implementation of the Interpreter pattern, ported from C++. Defines a grammar for a language and provides an interpreter to deal with this grammar. Includes a mathematical expression evaluator and a business rule engine example.

##### Setup and Usage
```bash
cd design-patterns/behavioral/interpreter
uv venv
. .venv/bin/activate
uv pip install -e ".[dev]"

# Run the main example
python -m interpreter_pattern

# Run the calculator example
python examples/calculator_example.py

# Run the rule engine example
python examples/rule_engine_example.py

# Run tests
pytest

# Run type checking
mypy src

# Run linting
ruff check src tests examples
```

#### [Visitor Pattern](design-patterns/behavioral/vistor/)
A Python implementation of the Visitor pattern, ported from C++. Allows adding new operations to existing object structures without modifying them. Includes geometric shape processing with multiple visitors for calculating area, perimeter, and generating descriptions.

##### Setup and Usage
```bash
cd design-patterns/behavioral/vistor
uv venv
. .venv/bin/activate
uv pip install -e ".[dev]"

# Run the main example
python -m visitor_pattern

# Run examples using launcher scripts
./run_visitor.py
./run_example.py

# Run tests
pytest

# Run linting
ruff check --fix .
```

#### [Strategy Pattern](design-patterns/behavioral/strategy/)
A Python implementation of the Strategy pattern, ported from C++. Defines a family of algorithms, encapsulates each one, and makes them interchangeable. Includes payment processing examples with multiple payment strategies like credit card, PayPal, and cryptocurrency.

##### Setup and Usage
```bash
cd design-patterns/behavioral/strategy
uv venv
. .venv/bin/activate
uv pip install -e ".[dev]"

# Run the main example
python -m strategy_pattern

# Run the interactive payment example
python examples/payment_example.py

# Or use the launcher script
./run_strategy_demo.py

# Run tests
pytest

# Run linting
ruff check .
```

## Concurrency Patterns

### [Pipeline](concurrency/pipelining/)
A Python implementation of the Pipeline concurrency pattern, ported from C++. Implements a thread-safe pipeline where each processing stage runs in its own thread. Data flows through stages sequentially, enabling parallel processing of different items at different stages. Includes generic stage definitions, thread-safe queues, and comprehensive examples.

#### Setup and Usage
```bash
cd concurrency/pipelining
uv venv
. .venv/bin/activate
uv pip install -e ".[dev]"

# Run the main example
python -m pipeline

# Run specific examples using launcher scripts
./run_pipeline.py
./run_data_example.py
./run_custom_example.py

# Run tests
pytest

# Run type checking
mypy src

# Run linting
ruff check --fix .
```

### [Readers-Writers](concurrency/reader-writer/)
A Python implementation of the Readers-Writers concurrency pattern, ported from C++. Provides a thread-safe way for multiple readers and writers to access a shared resource, with writer preference to prevent writer starvation. Includes thread-safe logging and RAII-style context management.

#### Setup and Usage
```bash
cd concurrency/reader-writer
uv venv
. .venv/bin/activate
uv pip install -e .

# Run the main example
python -m reader_writer

# Run specific examples
python run_basic_example.py
python run_advanced_example.py

# Run tests
pytest

# Run type checking
mypy src

# Run linting
ruff check --fix .
```

### [Producer-Consumer](concurrency/producer-consumer/)
A Python implementation of the Producer-Consumer concurrency pattern, ported from C++. Provides a thread-safe queue with multiple producers and consumers, with condition variables for efficient thread coordination. Includes generic type support, bounded queue with backpressure, and comprehensive thread management.

#### Setup and Usage
```bash
cd concurrency/producer-consumer
uv venv
. .venv/bin/activate
uv pip install -e ".[dev]"

# Run the main example
python -m producer_consumer

# Run specific examples using launcher scripts
./run_producer_consumer.py
./run_custom_example.py

# Run tests
pytest

# Run type checking
mypy src

# Run linting
ruff check --fix .
```

### [Thread Pool](concurrency/thread-pool/)
A Python implementation of the Thread Pool concurrency pattern, ported from C++. Manages a collection of worker threads that can execute tasks asynchronously, providing an efficient way to parallelize work across multiple threads. Includes Future-based result handling, exception propagation, and clean shutdown mechanism.

#### Setup and Usage
```bash
cd concurrency/thread-pool
uv venv
. .venv/bin/activate
uv pip install -e .

# Run the main example
python -m thread_pool

# Run specific examples using launcher scripts
./run_thread_pool.py
./examples/basic_usage.py
./examples/advanced_usage.py

# Run tests
pytest

# Run linting
ruff check .
```

### [Barrier Pattern](concurrency/barrier-example/)
A Python implementation of the Barrier concurrency pattern, ported from C++. Provides a synchronization mechanism to ensure multiple threads wait for each other to reach a specific point before proceeding further. Includes both a custom implementation using locks and condition variables, and a modern implementation using Python's threading.Barrier.

#### Setup and Usage
```bash
cd concurrency/barrier-example
uv venv
. .venv/bin/activate
uv pip install -e ".[dev]"

# Run the main example
python -m barrier_example

# Run specific examples using launcher scripts
./barrier_example_run.py
./examples/custom_example.py
./examples/modern_example.py

# Run tests
pytest

# Run type checking
mypy .

# Run linting
ruff check .
ruff format .
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