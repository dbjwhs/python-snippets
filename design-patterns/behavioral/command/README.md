# Command Pattern Implementation

The Command pattern, introduced in the Gang of Four's seminal 1994 book "Design Patterns: Elements of Reusable Object-Oriented Software," is a behavioral design pattern that turns requests into stand-alone objects. It was first notably used in the early 1980s in the Smalltalk-80 system for implementing the user interface, where commands were used to implement undoable operations. Today, it's ubiquitous in modern software development, found in everything from text editors (Microsoft Word's undo system) to game development (for input handling and replay systems) to distributed systems (for implementing message queues and transaction management). The pattern's versatility is demonstrated well by comparing a Document editing system with a SmartDevice home automation system - while these domains seem quite different at first glance (text manipulation vs. device control), they can both be elegantly implemented using the Command pattern, encapsulating operations like text insertion or temperature changes as command objects. The pattern is particularly prevalent in GUI applications, where each button or menu item typically encapsulates a command object.

The Command pattern offers several significant advantages. First, it decouples the object that invokes the operation from the objects that know how to perform it, promoting loose coupling and single responsibility. Second, it makes it easy to add new commands without changing existing code, following the Open-Closed Principle. Third, it enables powerful features like undo/redo, command logging, and transaction management. Fourth, it allows for command queuing, scheduling, and remote execution. Finally, it supports composite commands (macros) where multiple commands can be combined into a single command.

## Python Implementation

This project provides a modern Python implementation of the Command pattern with type hints and full test coverage. It includes:

- Type-annotated implementation with Python 3.10+ support
- Comprehensive unit tests with pytest
- Clean separation of concerns through SOLID principles
- Multiple real-world examples (document editing and smart home automation)
- Fully documented with docstrings

### Installation

```bash
# Create a virtual environment with uv (install uv if you don't have it)
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install using pip
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Implementation Details

### Core Components
1. **Command**: Abstract base class declaring the execution interface
2. **Concrete Commands**: Implement the Command interface for specific operations
3. **Invoker**: Asks the command to carry out the request
4. **Receiver**: Knows how to perform the actual operations
5. **Client**: Creates and configures concrete command objects

### Best Practices
- Keep commands small and focused
- Make commands immutable after creation
- Use the Memento pattern for complex undo operations
- Consider using the Prototype pattern for command cloning
- Implement command validation before execution
- Use command factories for complex command creation

### Common Pitfalls
- Creating too large or complex commands
- Mixing command execution logic with command state
- Not handling edge cases in undo operations
- Storing too much state in commands
- Ignoring error handling in command execution
- Not considering memory implications of command history

### When to Use
- Implementing undo/redo functionality
- Parameterizing objects with operations
- Supporting logging, queuing, or transaction management
- Implementing callback functionality
- Creating menu systems or macro recording
- Need for asynchronous or delayed execution

### When Not to Use
- Simple operations that don't need undoing
- When direct method calls are clearer
- When command overhead isn't justified
- Real-time systems with strict performance requirements
- Very simple applications with basic functionality

## Example Use Cases

### Document Editing
```python
doc = Document()
editor = DocumentEditor(doc)

editor.execute_command(InsertCommand(doc, "Hello", 0))
editor.execute_command(InsertCommand(doc, " World", 5))
print(doc.content)  # Outputs: "Hello World"

editor.undo()  # Undoes the last command
print(doc.content)  # Outputs: "Hello"
```

### Smart Home Automation
```python
# Create devices and home automation system
light = SmartDevice("Living Room Light")
thermostat = SmartDevice("Thermostat")
home = HomeAutomationSystem()

# Create a scene with multiple commands
movie_scene = SceneCommand()
movie_scene.add_command(PowerCommand(light, False))  # Turn off lights
movie_scene.add_command(SetTemperatureCommand(thermostat, 22))  # Set temperature

# Store the scene and activate it later
home.create_scene("movie_time", movie_scene)
home.activate_scene("movie_time")

# Undo the scene activation
home.undo_last()
```

### Running the Examples

```bash
# Document editing example
python -m command_pattern.examples.document_example

# Smart home automation example
python -m command_pattern.examples.smart_home_example
```

## Testing Considerations
- Test both execute and undo operations
- Verify command state after undo/redo
- Test command composition
- Check edge cases and error conditions
- Verify command history management
- Test concurrent command execution if applicable

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=command_pattern

# Run type checking
mypy src tests

# Run linting
ruff check src tests
```

## Performance Considerations
- Memory usage for command history
- Command object creation overhead
- Undo/redo stack limitations
- Serialization impact for persistent commands
- Impact of command validation
- Memory leaks in command cleanup

## Extended Features
- Command composition for macro operations
- Command serialization for persistence
- Asynchronous command execution
- Progress monitoring and cancellation
- Command validation and authorization
- Command logging and analytics

## Maintenance Tips
- Keep command classes small and focused
- Document command preconditions and postconditions
- Implement proper error handling
- Use meaningful command names
- Consider command versioning for long-lived systems
- Implement proper cleanup in destructors

## License
This implementation is provided under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please feel free to submit pull requests with improvements or bug fixes.