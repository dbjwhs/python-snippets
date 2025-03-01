# MIT License
# Copyright (c) 2025 dbjwhs

import pytest
from src.lru_cache_simple import LRUCache, VALUE_NOT_FOUND


def test_constructor_validation():
    """Test that the constructor validates capacity correctly."""
    with pytest.raises(ValueError):
        LRUCache(-1)


def test_basic_functionality():
    """Test the basic functionality as described in the original problem."""
    cache = LRUCache(3)
    assert cache.empty is True
    
    # cache.put(1,1)
    cache.put(1, 1)
    assert cache.size == 1
    assert cache.get(1) == 1
    
    # cache.put(2,2)
    # cache.put(1,3)
    cache.put(2, 2)
    cache.put(1, 3)  # Update existing key
    assert cache.size == 2
    
    # cache.get(1) -> returns 3
    assert cache.get(1) == 3
    
    # cache.put(3,4)
    # cache.put(4,3) -> removes key 2
    # cache.get(2) -> returns -1
    cache.put(3, 4)
    cache.put(4, 3)  # This should evict key 2
    assert cache.get(2) == VALUE_NOT_FOUND


def test_capacity_eviction():
    """Test that items are evicted based on capacity."""
    cache = LRUCache(3)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)
    
    # Should evict key 1
    cache.put(4, 4)
    assert cache.get(1) == VALUE_NOT_FOUND
    
    # Verify all cache entries are valid
    assert cache.get(2) == 2
    assert cache.get(3) == 3
    assert cache.get(4) == 4


def test_ordering():
    """Test that the LRU ordering works correctly."""
    cache = LRUCache(3)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)
    
    # Make 1 the most recently used
    assert cache.get(1) == 1
    
    # Should evict 2, not 1
    cache.put(4, 4)
    
    assert cache.get(1) != VALUE_NOT_FOUND
    assert cache.get(2) == VALUE_NOT_FOUND
    assert cache.get(3) == 3
    assert cache.get(4) == 4


def test_generic_type_support():
    """Test that the cache supports different key and value types."""
    # String keys, int values
    cache_str_int = LRUCache[str, int](2)
    cache_str_int.put("one", 1)
    cache_str_int.put("two", 2)
    assert cache_str_int.get("one") == 1
    
    # Int keys, string values
    cache_int_str = LRUCache[int, str](2)
    cache_int_str.put(1, "one")
    cache_int_str.put(2, "two")
    assert cache_int_str.get(1) == "one"