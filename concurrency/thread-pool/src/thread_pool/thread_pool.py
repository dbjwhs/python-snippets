#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Modern Python implementation of a Thread Pool for concurrent task execution.
"""

import concurrent.futures
import threading
import time
from collections.abc import Callable
from concurrent.futures import Future
from enum import Enum
from queue import Queue
from threading import Condition, Lock, Thread
from typing import Any, Optional, TypeVar

from icecream import ic

# Type variable for the return type of the task
T = TypeVar('T')


class LogLevel(Enum):
    """Log level enumeration for the logger."""
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


class Logger:
    """Thread-safe logger implementation."""
    _instance: Optional['Logger'] = None
    _lock: Lock = Lock()

    def __init__(self) -> None:
        """Initialize the logger."""
        self._log_lock = Lock()

    @classmethod
    def get_instance(cls) -> 'Logger':
        """Get the singleton instance of the logger."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def log(self, level: LogLevel, *messages: Any) -> None:
        """
        Log a message with the specified log level.
        
        Args:
            level: The log level of the message
            messages: The message components to log
        """
        with self._log_lock:
            thread_id = threading.get_ident()
            message = " ".join(str(msg) for msg in messages)
            ic(f"[{level.name}] [{thread_id}] {message}")


def thread_id_to_string(thread: Thread | None = None) -> str:
    """
    Convert a thread ID to a string representation.
    
    Args:
        thread: The thread to get the ID from (defaults to current thread)
        
    Returns:
        String representation of the thread ID
    """
    if thread is None:
        return str(threading.get_ident())
    return str(thread.ident) if thread.ident is not None else "unknown"


class ThreadPool:
    """
    Thread pool implementation for managing worker threads that can execute tasks asynchronously.
    """
    
    def __init__(self, num_threads: int, logger: Logger) -> None:
        """
        Initialize the thread pool with the specified number of worker threads.
        
        Args:
            num_threads: Number of worker threads to create
            logger: Logger instance for logging
        """
        self._workers: list[Thread] = []
        self._tasks: Queue[Callable[[], None]] = Queue()
        self._queue_mutex: Lock = Lock()
        self._condition: Condition = Condition(self._queue_mutex)
        self._stop: bool = False
        self._logger: Logger = logger
        
        self._logger.log(LogLevel.INFO, f"Initializing thread pool with {num_threads} threads")
        
        # Create worker threads
        for i in range(num_threads):
            worker = Thread(target=self._worker_thread)
            worker.daemon = True  # Set as daemon so they don't block program exit
            self._workers.append(worker)
            worker.start()
            self._logger.log(LogLevel.INFO, f"Created worker thread {thread_id_to_string(worker)}")
    
    def __del__(self) -> None:
        """Ensure thread pool is properly shut down."""
        self.shutdown()
    
    def shutdown(self) -> None:
        """Shut down the thread pool and wait for all threads to complete."""
        with self._queue_mutex:
            if self._stop:
                return
            self._stop = True
            self._logger.log(LogLevel.INFO, "Initiating thread pool shutdown")
        
        # Wake up all threads
        with self._condition:
            self._condition.notify_all()
        
        # Wait for all threads to finish
        for worker in self._workers:
            if worker.is_alive():
                worker.join()
                self._logger.log(LogLevel.INFO, f"Worker thread {thread_id_to_string(worker)} joined")
        
        self._logger.log(LogLevel.INFO, "Thread pool shutdown complete")
    
    def _worker_thread(self) -> None:
        """Worker thread function that processes tasks from the queue."""
        while True:
            with self._condition:
                # Wait for tasks or stop signal
                while not self._stop and self._tasks.empty():
                    self._condition.wait()
                
                # Exit if stopped and no tasks remain
                if self._stop and self._tasks.empty():
                    self._logger.log(LogLevel.INFO, f"Worker thread {thread_id_to_string()} shutting down")
                    return
                
                # Get next task from queue
                task = self._tasks.get()
                self._logger.log(LogLevel.INFO, f"Worker thread {thread_id_to_string()} dequeued a task")
            
            # Execute the task
            if task:
                task()
                self._tasks.task_done()
    
    def enqueue(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> Future[T]:
        """
        Enqueue a task for execution by a worker thread.
        
        Args:
            func: The callable to execute
            *args: Arguments to pass to the callable
            **kwargs: Keyword arguments to pass to the callable
            
        Returns:
            A Future representing the result of the task
            
        Raises:
            RuntimeError: If trying to enqueue on a stopped ThreadPool
        """
        future: Future[T] = concurrent.futures.Future()
        
        def task_wrapper() -> None:
            if future.cancelled():
                return
                
            try:
                result = func(*args, **kwargs)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
        
        with self._queue_mutex:
            if self._stop:
                raise RuntimeError("Cannot enqueue on stopped ThreadPool")
            
            self._tasks.put(task_wrapper)
            self._logger.log(LogLevel.INFO, "Task enqueued")
        
        # Notify one waiting thread
        with self._condition:
            self._condition.notify()
        
        return future


# Module execution sample code
def main() -> None:
    """Main function demonstrating thread pool usage."""
    logger = Logger.get_instance()
    
    try:
        # Thread pool will use maximum number of concurrent threads supported
        import os
        thread_count = max(4, os.cpu_count() or 4)
        
        logger.log(LogLevel.INFO, f"This machine supports {thread_count} concurrent threads")
        
        # List to store future results
        results: list[Future[int]] = []
        
        # Create thread pool with worker threads
        pool = ThreadPool(thread_count, logger)
        
        # Add tasks to the thread pool
        for i in range(thread_count * 2):
            # Enqueue task that logs thread id and returns square of input
            future = pool.enqueue(
                lambda captured_i=i: (
                    logger.log(
                        LogLevel.INFO, 
                        f"Task {captured_i} running on thread {thread_id_to_string()}"
                    ),
                    time.sleep(1),  # Do some work
                    captured_i * captured_i
                )[-1]  # Return the last item from the tuple (i * i)
            )
            results.append(future)
        
        # Get and print results
        for i, future in enumerate(results):
            logger.log(LogLevel.INFO, f"Result {i}: {future.result()}")
        
        # Explicitly shut down the pool (would happen in __del__ too)
        pool.shutdown()
        
    except Exception as e:
        # Handle any exceptions
        logger.log(LogLevel.CRITICAL, f"Error: {str(e)}")
        return
    
    logger.log(LogLevel.INFO, "Thread pool demonstration completed successfully.")


if __name__ == "__main__":
    main()