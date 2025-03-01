# python-snippets
A mono repo to contain my personal snippets for Python, with most my endeavor to port my C++ snippets to Python.

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
