# MIT License
# Copyright (c) 2025 dbjwhs

"""Thread-safe queue implementation for the pipeline pattern."""

import threading
from queue import Queue
from typing import Any, Generic, TypeVar, cast

T = TypeVar('T')


class SafeQueue(Generic[T]):
    """
    Thread-safe queue implementation that handles concurrent access to data.
    
    This is a generic class that can store any type T.
    """

    def __init__(self) -> None:
        """Initialize a new SafeQueue instance."""
        self._queue: Queue[T] = Queue()
        self._mutex = threading.RLock()
        self._condition = threading.Condition(self._mutex)
        self._done = False
    
    def push(self, item: T) -> None:
        """
        Add an item to the queue in a thread-safe manner.
        
        Args:
            item: The item to add to the queue
        """
        with self._mutex:
            self._queue.put(item)
            self._condition.notify()
    
    def pop(self, item: T) -> bool:
        """
        Remove and return an item from the queue.
        
        Args:
            item: Reference that will be updated with the popped value
            
        Returns:
            False if queue is empty and done, True otherwise
            
        Note:
            This method doesn't actually use the 'item' parameter.
            Instead it returns the popped value as a tuple (bool, T).
            The caller should use a mutable container to capture the value.
        """
        with self._condition:
            while self._queue.empty() and not self._done:
                self._condition.wait()
            
            if self._queue.empty():
                return False
            
            # In Python, we can't update the reference to the passed parameter
            # Instead, we use a container (list) to hold the value
            # The caller should pass a list with a single element
            # and we'll update the value of that element
            
            # Assuming item is actually a list with a single element
            item_list = cast(list, item)
            item_list[0] = self._queue.get()
            return True
    
    def set_done(self) -> None:
        """Signal that no more items will be added to the queue."""
        with self._mutex:
            self._done = True
            self._condition.notify_all()
    
    def is_empty(self) -> bool:
        """
        Check if the queue is empty.
        
        Returns:
            True if the queue is empty, False otherwise
        """
        with self._mutex:
            return self._queue.empty()