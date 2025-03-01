# Binary Search Tree Implementation

##  🚧 🚧

### Under Construction

### Future Improvements Required

Attention readers of the code the following will be added soon.

1. Add removal operations
2. Implement balancing (AVL or Red-Black)
3. Add iterator support
4. Add serialization/deserialization (*mainly for data persistence to disk*)
5. Add range queries
6. And **finally**, improve logging system; currently logging is basic. The Best would be to add as an **observer pattern**, an observer of tree operations.
   - Separates logging concerns from tree operations
   - Makes it easy to add/remove logging at runtime 
   - Allows for multiple observers (could have logging + metrics + etc.)
   - Keeps the core tree operations clean and focused

##  🚧 🚧

---

## What is a Binary Search Tree (BST)?

A Binary Search Tree (BST) is a hierarchical data structure composed of nodes where each node stores a value and references to two children. BSTs enforce a specific ordering property:

- For any node N, all values in its left subtree are strictly less than N's value
- For any node N, all values in its right subtree are strictly greater than N's value
- No duplicate values are allowed

This ordering makes BSTs efficient for searching, as each comparison allows you to eliminate half of the remaining tree from consideration.

Example of a valid BST:
```
        5
      /   \
     3     7    // 3 < 5 < 7
    / \   / \
   2   4 6   8  // 2 < 3 < 4, 6 < 7 < 8
```

## Performance Characteristics

Time Complexities:
- Search: O(log n) - when balanced
- Insert: O(log n) - when balanced
- Delete: O(log n) - when balanced
- Traversal: O(n) - must visit all nodes

where n is the number of nodes in the tree.

Note: These O(log n) complexities assume the tree is relatively balanced. In the worst case (completely unbalanced tree), operations can degrade to O(n).

Space Complexity:
- O(n) for storing n nodes
- O(h) for recursive operations (where h is tree height)

## Use Cases

BSTs are commonly used in:
1. Implementing Symbol Tables and Dictionaries
2. Database Indexing
3. File System Organization
4. Auto-complete and Spell Checkers
5. Priority Queues
6. Expression Parsers

## Implementation Details

### Key Features
- Generic implementation supporting any comparable type
- Type hints using Python's typing system
- Comprehensive traversal options (in-order, pre-order, post-order)
- BST property validation
- Support for any type that implements `<` operator

### Traversal Options
Three traversal methods are provided:
1. In-order (Left-Root-Right) - visits nodes in ascending order
2. Pre-order (Root-Left-Right) - useful for copying trees
3. Post-order (Left-Right-Root) - useful for deletion

### Visitor Pattern
Traversals use the visitor pattern allowing flexible node processing:
```python
tree.in_order_traversal(lambda value: print(value))
```

## Usage Examples

### Basic Operations
```python
from binary_tree import BinaryTree

tree = BinaryTree[int]()

# Insert values
tree.insert(5)
tree.insert(3)
tree.insert(7)

# Search
found = tree.search(3)  # returns True

# Find min/max
min_val = tree.find_min_value()  # returns 3
max_val = tree.find_max_value()  # returns 7
```

### Working with Strings
```python
from binary_tree import BinaryTree

string_tree = BinaryTree[str]()

string_tree.insert("hello")
string_tree.insert("world")
string_tree.insert("abc")

# Traversal with custom processing
string_tree.in_order_traversal(lambda s: print(s))  # prints: "abc hello world"
```

## Implementation Notes

### BST Property Validation
- Uses optional min/max bounds for validation
- Works with any comparable type
- Validates entire tree structure recursively

### Generic Type Support
- Works with any type supporting the `<` operator
- No requirement for `==` operator
- Consistent behavior across different types

## Best Practices
1. Check for an empty tree before operations
2. Use the appropriate traversal for your use case
3. Consider balance if performance critical
4. Use custom comparators for complex types

## Thread Safety
This implementation is not thread-safe. External synchronization is required for concurrent operations.

## Error Handling
- Raises RuntimeError for operations on empty trees
- Returns False for failed searches
- Silently ignores duplicate insertions

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! Please feel free to submit pull requests with improvements or bug fixes.

## Development Setup

### Prerequisites
- Python 3.10 or higher
- UV package manager

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/binary-tree.git
cd binary-tree

# Create virtual environment and install dependencies
uv venv
. .venv/bin/activate
uv pip install -e ".[dev]"
```

### Running Tests
```bash
pytest
```

### Linting
```bash
ruff check .
```