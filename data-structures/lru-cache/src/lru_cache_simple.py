# MIT License
# Copyright (c) 2025 dbjwhs

from collections import OrderedDict
from typing import Dict, Optional, TypeVar, Generic, Any

K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type

VALUE_NOT_FOUND = -1
ENABLE_DEBUG = False


class LRUCache(Generic[K, V]):
    """
    An implementation of a Least Recently Used (LRU) cache.
    
    This implementation has O(1) time complexity for both get and put operations.
    """
    
    def __init__(self, capacity: int) -> None:
        """
        Initialize the LRU cache with the given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
            
        Raises:
            ValueError: If capacity is less than or equal to zero
        """
        if capacity <= 0:
            raise ValueError("Cache capacity must be greater than zero")
            
        self._capacity: int = capacity
        # Using OrderedDict as it maintains insertion order and provides O(1) operations
        self._cache: OrderedDict[K, V] = OrderedDict()
        
        if ENABLE_DEBUG:
            print(f"DEBUG: Created LRU cache with capacity {self._capacity}")
    
    def get(self, key: K) -> Any:
        """
        Retrieves the value associated with the given key if it exists in the cache.
        
        Args:
            key: The key to look up
            
        Returns:
            The value associated with the key, or VALUE_NOT_FOUND if the key is not in the cache
        """
        if ENABLE_DEBUG:
            print(f"DEBUG: GET operation - key: {key}")
            
        if key not in self._cache:
            if ENABLE_DEBUG:
                print(f"DEBUG: Key {key} not found in cache")
                self._print_cache_state()
            return VALUE_NOT_FOUND
            
        # Move to end (most recently used position) and return value
        value = self._cache[key]
        self._cache.move_to_end(key)
        
        if ENABLE_DEBUG:
            print(f"DEBUG: Found value {value} for key {key}")
            self._print_cache_state()
            
        return value
    
    def put(self, key: K, value: V) -> None:
        """
        Inserts or updates a key-value pair in the cache.
        
        If the key already exists, its value is updated and it becomes the most recently used item.
        If the key doesn't exist and the cache is at capacity, the least recently used item is removed.
        
        Args:
            key: The key to insert or update
            value: The value to associate with the key
        """
        if ENABLE_DEBUG:
            print(f"DEBUG: PUT operation - key: {key}, value: {value}")
            
        # Check if the key already exists
        if key in self._cache:
            if ENABLE_DEBUG:
                print(f"DEBUG: Updating existing key {key} with new value {value}")
                
            # Update the value and move it to the end (most recently used)
            self._cache[key] = value
            self._cache.move_to_end(key)
            
            if ENABLE_DEBUG:
                self._print_cache_state()
            return
            
        # If cache is full, remove the least recently used item (first item in OrderedDict)
        if len(self._cache) == self._capacity:
            # popitem with last=False removes the first item (least recently used)
            least_recent_key, _ = self._cache.popitem(last=False)
            
            if ENABLE_DEBUG:
                print(f"DEBUG: Cache full, removing LRU item with key {least_recent_key}")
                
        # Add the new key-value pair (automatically becomes most recently used)
        self._cache[key] = value
        
        if ENABLE_DEBUG:
            print(f"DEBUG: Added new entry - key: {key}, value: {value}")
            self._print_cache_state()
    
    def _print_cache_state(self) -> None:
        """Prints the current state of the cache for debugging"""
        if ENABLE_DEBUG:
            cache_items = list(self._cache.items())
            print(f"DEBUG: Cache state [", end="")
            for k, v in cache_items:
                print(f" ({k}:{v})", end="")
            print(" ]")
    
    @property
    def size(self) -> int:
        """Returns the current number of items in the cache"""
        return len(self._cache)
        
    @property
    def empty(self) -> bool:
        """Returns True if the cache is empty, False otherwise"""
        return len(self._cache) == 0


if __name__ == "__main__":
    # Enable debug mode for interactive testing
    ENABLE_DEBUG = True
    print("DEBUG: All tests moved to pytest test files")