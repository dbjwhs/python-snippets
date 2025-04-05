# Python Object Copying Pitfalls

## Overview
While Python doesn't have object slicing in the same way as C++, it has similar pitfalls related to object copying, improper inheritance, and serialization. This project demonstrates these issues that can cause loss of data or behavior in object-oriented Python code.

## The Problem
Python's object model differs from C++, but similar issues arise when:
- Using incorrect inheritance patterns or improper `super()` calls
- Relying on shallow copying with complex objects
- Serializing and deserializing objects without proper type information
- Using duck typing without proper runtime type checking

## Example Code
```python
from abc import ABC, abstractmethod

class Base(ABC):
    def __init__(self):
        self.base_data = "Base data"
    
    @abstractmethod
    def print(self):
        pass

class Derived(Base):
    def __init__(self):
        super().__init__()
        self.derived_data = "Derived data"
        self.base_data = "Modified base data"
    
    def print(self):
        print(f"Derived with: {self.base_data} and {self.derived_data}")

# Case 1: By reference - SAFE, Python uses references by default
def process_by_reference(obj: Base):
    print("Processing by reference: ")
    obj.print()  # Works correctly with polymorphism

# Case 2: Improper inheritance - DANGEROUS
class ImproperInheritance(Derived):
    def __init__(self):
        # This calls Base.__init__() directly, skipping Derived.__init__()
        Base.__init__(self)
        self.improper_data = "Improper data"
    
    def print(self):
        # Will be missing derived_data initialization
        print(f"Improper with: {self.base_data} and {self.improper_data}")
```

## Prevention
To prevent these issues in Python:
1. Always use proper inheritance patterns with `super().__init__()` calls
2. Be aware of the difference between shallow and deep copying
3. Implement proper serialization/deserialization with type information
4. Use appropriate type hints and runtime type checking
5. Consider using dataclasses or attrs for cleaner data handling

## Common Bug Patterns
These issues often appear in these scenarios:
1. Incorrect inheritance chains in complex class hierarchies
2. Inconsistent serialization formats across an application
3. Mixing different copying strategies (shallow/deep)
4. Using duck typing without appropriate runtime checks

## Best Practices
```python
# Bad - improper inheritance
class WrongDerived(Base):
    def __init__(self):
        Base.__init__(self)  # Skips intermediate classes

# Good - proper inheritance
class ProperDerived(Base):
    def __init__(self):
        super().__init__()  # Correctly follows MRO

# Bad - assumes shallow copying is sufficient
from copy import copy
copied = copy(complex_object)

# Good - uses deep copying for complex structures
from copy import deepcopy
copied = deepcopy(complex_object)

# Bad - loses type information in serialization
json_data = json.dumps(obj.__dict__)

# Good - preserves type information
json_data = json.dumps({"type": obj.__class__.__name__, "data": obj.__dict__})
```

## Debugging Tips
If you suspect object copying issues:
1. Add debug logging to initialization methods
2. Check object types with `isinstance()` before and after operations
3. Use `vars()` or `dir()` to inspect object attributes
4. Implement proper `__repr__` methods for better debugging

## Further Reading
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
- [Python's super() explained](https://realpython.com/python-super/)
- [Copy in Python](https://docs.python.org/3/library/copy.html)
- [Pickle documentation](https://docs.python.org/3/library/pickle.html)

## Contributing

Feel free to contribute additional examples or common pitfall scenarios you've encountered. These issues remain common
in Python codebases, and sharing experiences helps the community.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.