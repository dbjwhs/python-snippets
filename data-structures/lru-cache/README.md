# LRU Cache

A Python implementation of an LRU (Least Recently Used) cache, a data structure that stores a limited number of items and discards the least recently used item when the cache becomes full.

## Overview

An LRU cache is a data structure that combines fast access with a policy for automatically removing the least recently accessed elements when the cache reaches its capacity limit. It operates on the principle that recently used items are likely to be used again in the near future.

## Features

- O(1) time complexity for both read and write operations
- Fixed capacity with automatic eviction of least recently used items
- Simple API with `get` and `put` operations
- Strong typing with generic type parameters
- Comprehensive pytest test suite
- Modern Python project structure with uv for package management
- Ruff for code linting

## History
The LRU cache algorithm was first introduced in the 1960s during the early days of computer memory management. It was developed to address the challenge of managing limited, fast-access memory resources (like CPU cache) effectively.

Key historical developments:
- 1965: First documented use in IBM's OS/360
- 1970s: Widely adopted in virtual memory systems
- 1980s: Became standard in CPU cache designs
- 1990s-present: Essential component in web browsers, database systems, and operating systems

## How It Works
LRU cache operates on these core principles:
1. Fixed Capacity: The cache has a maximum number of items it can hold
2. Fast Access: Both reads and writes should be O(1) operations
3. Tracking Usage: Each access to a cached item marks it as "most recently used"
4. Eviction Policy: When full, the cache removes the least recently used item

## Implementation Details
This Python implementation uses:
- OrderedDict: Python's built-in ordered dictionary that maintains insertion order and provides O(1) lookups

## Usage Example
```python
from src.lru_cache_simple import LRUCache

# Create a cache with capacity 3
cache = LRUCache(3)

# Add items
cache.put(1, 1)
cache.put(2, 2)
cache.put(3, 3)

# Get an item (makes it the most recently used)
value = cache.get(1)  # Returns 1

# Add a new item when at capacity (evicts least recently used)
cache.put(4, 4)  # This will evict key 2

# Key 2 is no longer in the cache
cache.get(2)  # Returns -1
```

## Type Safety
The implementation uses Python's generic type hints:

```python
# String keys, integer values
cache = LRUCache[str, int](3)
cache.put("key1", 42)

# Integer keys, string values
cache = LRUCache[int, str](3) 
cache.put(1, "value")
```

## Getting Started

### Installation
Clone this repository, then install with uv:

```bash
git clone <repository-url>
cd python-snippets/data-structures/lru-cache
uv venv
uv pip install -e ".[dev]"
```

### Running Tests
```bash
python -m pytest
```

### Linting
```bash
ruff check .
```

## License

This code is provided under the MIT License. Feel free to use, modify, and distribute as needed.

## Legacy C++ Implementation

A C++ implementation is also available in the `cp-ex` directory. This was the original implementation that was ported to Python.