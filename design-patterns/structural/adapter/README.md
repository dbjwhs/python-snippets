# Adapter Design Pattern

The Adapter pattern is a structural design pattern that allows objects with incompatible interfaces to collaborate. First introduced in the book "Design Patterns: Elements of Reusable Object-Oriented Software" by the Gang of Four in 1994, it acts as a wrapper between two objects. The pattern converts the interface of one class into another interface that clients expect, enabling classes to work together that couldn't otherwise because of incompatible interfaces. Think of it like a power adapter that allows you to charge your devices in different countries - it doesn't change the underlying electricity or your device, it just makes them work together.

## Use Cases & Problem Solving

The Adapter pattern is particularly useful in scenarios where:
- You need to integrate new systems with legacy code
- You're working with multiple existing systems that need to communicate
- You want to create reusable code that depends on objects with different interfaces
- You need to make independently developed classes work together
- You're integrating third-party libraries or SDKs
- You're dealing with multiple data formats or protocols

Common problems it solves include:
- Incompatible interfaces between systems
- Legacy system integration
- Multiple version support
- Cross-platform compatibility
- Data format conversion
- Protocol translation

## Implementation Examples

### Basic Structure
```python
# Target interface (Protocol in Python)
class Target(Protocol):
    def request(self) -> None:
        ...

# Adaptee (incompatible interface)
class Adaptee:
    def specific_request(self) -> None:
        # Different interface implementation
        pass

# Adapter
class Adapter(Target):
    def __init__(self) -> None:
        self._adaptee = Adaptee()
    
    def request(self) -> None:
        self._adaptee.specific_request()
```

### Real-World Examples
1. Database Adapters
2. Payment Gateway Integration
3. Multi-platform GUI Systems
4. File System Operations (as shown in this implementation)
5. Network Protocol Conversion

## Best Practices

### Do's
- Keep the adapter simple and focused on interface translation
- Use composition over inheritance when possible
- Create clear separation between business logic and adaptation
- Document the expected behavior of both interfaces
- Consider using the Adapter pattern in conjunction with Factory pattern
- Write comprehensive tests for the adaptation layer

### Don'ts
- Don't add new functionality in the adapter
- Avoid complex adaptation logic
- Don't modify the adaptee's code if possible
- Don't create adapters for adapters
- Don't use adapters when interfaces are similar

## Installation and Setup

```bash
# Clone the repository
git clone <repository-url>
cd adapter-pattern

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Unix/Linux
# Or on Windows:
# .venv\Scripts\activate

# Install the package in development mode
uv pip install -e ".[dev]"
```

## Usage Examples

### Running the Main Examples
```bash
# Run the main demo
python -m adapter_pattern

# Or use the provided script
./run_adapter_demo.py
```

### Running Specific Examples
```bash
# Run file system example
python -m adapter_pattern.examples.file_system_example

# Run basic adapter example
python -m adapter_pattern.examples.basic_adapter_example

# Use executable scripts
./run_file_system_example.py
./run_basic_example.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_adapter.py
```

### Linting
```bash
# Run ruff for linting
ruff check .

# Auto-fix issues
ruff check --fix .
```

## License

This code is provided under the MIT License. Feel free to use, modify, and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.