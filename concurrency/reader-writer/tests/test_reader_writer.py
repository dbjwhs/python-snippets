# MIT License
# Copyright (c) 2025 dbjwhs

import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from reader_writer.reader_writer import ReadersWriters
from reader_writer.utils import LogLevel, Logger


@pytest.fixture
def logger():
    """Create a logger instance for testing."""
    return Logger.get_instance()


@pytest.fixture
def readers_writers():
    """Create a ReadersWriters instance for testing."""
    return ReadersWriters()


def test_reader_writer_initialization(readers_writers):
    """Test that the ReadersWriters class initializes correctly."""
    assert readers_writers._active_readers == 0
    assert readers_writers._waiting_readers == 0
    assert readers_writers._is_writing is False
    assert readers_writers._waiting_writers == 0
    assert readers_writers._shared_resource == 0


def test_multiple_readers_concurrency(readers_writers, logger):
    """Test that multiple readers can access the resource concurrently."""
    num_readers = 10
    active_readers = []
    read_lock = threading.Lock()
    
    def reader_task():
        readers_writers.start_read()
        with read_lock:
            active_readers.append(1)
        # Simulate read operation
        time.sleep(0.05)
        with read_lock:
            active_readers.pop()
        readers_writers.end_read()
    
    # Start all readers concurrently
    threads = []
    for _ in range(num_readers):
        thread = threading.Thread(target=reader_task)
        threads.append(thread)
        thread.start()
    
    # Check if multiple readers are active at the same time
    time.sleep(0.01)  # Give time for threads to start
    with read_lock:
        assert len(active_readers) > 1, "Expected multiple active readers"
    
    # Wait for all readers to finish
    for thread in threads:
        thread.join()


def test_writer_exclusivity(readers_writers, logger):
    """Test that only one writer can access the resource at a time."""
    num_writers = 5
    active_writers = []
    write_lock = threading.Lock()
    
    def writer_task(value):
        readers_writers.start_write()
        with write_lock:
            active_writers.append(1)
            # There should never be more than one active writer
            assert len(active_writers) == 1, "Expected only one active writer"
        
        # Simulate write operation
        readers_writers._shared_resource = value
        time.sleep(0.05)
        
        with write_lock:
            active_writers.pop()
        readers_writers.end_write()
    
    # Start all writers concurrently
    with ThreadPoolExecutor(max_workers=num_writers) as executor:
        for i in range(num_writers):
            executor.submit(writer_task, i)


def test_writer_blocks_readers(readers_writers, logger):
    """Test that readers are blocked when a writer is active."""
    # Setup control events
    writer_done_event = threading.Event()
    writer_has_lock = threading.Event()
    reader_tried_lock = threading.Event()
    reader_got_lock = threading.Event()
    
    # First get a writer lock
    def writer_thread_func():
        # Get the write lock
        readers_writers.start_write()
        # Signal that we have the lock
        writer_has_lock.set()
        # Wait for a while holding the lock
        time.sleep(0.2)
        # Release the lock
        readers_writers.end_write()
        # Signal we're done
        writer_done_event.set()
    
    # Create a reader that will try to get the lock after the writer
    def reader_thread_func():
        # Wait until writer signals it has the lock
        writer_has_lock.wait()
        
        # Signal we're attempting to get the lock
        reader_tried_lock.set()
        
        # Try to get read lock (this should block)
        readers_writers.start_read()
        
        # We got the lock, signal it
        reader_got_lock.set()
        
        # Release it
        readers_writers.end_read()
    
    # Start the threads
    writer_thread = threading.Thread(target=writer_thread_func)
    reader_thread = threading.Thread(target=reader_thread_func)
    
    writer_thread.start()
    reader_thread.start()
    
    # Wait for writer to get the lock
    writer_has_lock.wait()
    
    # Wait for reader to try to get the lock
    reader_tried_lock.wait()
    
    # Give the reader a moment to potentially acquire the lock (it shouldn't)
    time.sleep(0.1)
    
    # Check that reader hasn't acquired the lock yet
    assert not reader_got_lock.is_set(), "Reader should be blocked while writer has lock"
    
    # Wait for writer to finish
    writer_done_event.wait()
    
    # Wait for reader to finish (should happen quickly once writer is done)
    reader_thread.join(timeout=0.5)
    
    # Check that the reader eventually got the lock
    assert reader_got_lock.is_set(), "Reader should have acquired lock after writer finished"


def test_writer_preference(readers_writers, logger):
    """Test that writers are given preference over readers."""
    writer_waiting = threading.Event()
    reader_waiting = threading.Event()
    reader_count = 0
    reader_lock = threading.Lock()
    read_allowed = threading.Event()
    
    # Start a reader to hold the read lock
    def initial_reader():
        readers_writers.start_read()
        # Let the test function know we have the read lock
        read_allowed.set()
        # Wait until the test function tells us to release
        time.sleep(0.1)
        readers_writers.end_read()
    
    initial_reader_thread = threading.Thread(target=initial_reader)
    initial_reader_thread.start()
    
    # Wait for initial reader to acquire read lock
    read_allowed.wait()
    
    # Now start a writer that will wait
    def waiting_writer():
        writer_waiting.set()  # Signal that writer is waiting
        readers_writers.start_write()  # This will block until reader releases
        
        # After acquiring write lock, check that no readers acquired lock before us
        with reader_lock:
            assert reader_count == 0, "Reader acquired lock before waiting writer"
        
        time.sleep(0.05)  # Hold the write lock briefly
        readers_writers.end_write()
    
    writer_thread = threading.Thread(target=waiting_writer)
    writer_thread.start()
    
    # Wait for writer to start waiting
    writer_waiting.wait()
    time.sleep(0.05)  # Give writer thread time to enter wait state
    
    # Now start a reader that should be blocked by the waiting writer
    def waiting_reader():
        reader_waiting.set()  # Signal that reader is waiting
        
        # Try to acquire read lock - this should be blocked by the waiting writer
        readers_writers.start_read()
        
        # If we got here, increment the reader count
        with reader_lock:
            nonlocal reader_count
            reader_count += 1
        
        readers_writers.end_read()
    
    reader_thread = threading.Thread(target=waiting_reader)
    reader_thread.start()
    
    # Wait for reader to start waiting
    reader_waiting.wait()
    
    # Wait for all threads to finish
    initial_reader_thread.join()
    writer_thread.join()
    reader_thread.join()


def test_read_resource_method(readers_writers, logger):
    """Test the read_resource method."""
    readers_writers._shared_resource = 42
    readers_writers.read_resource(logger)
    assert readers_writers._active_readers == 0, "Read lock not properly released"


def test_write_resource_method(readers_writers, logger):
    """Test the write_resource method."""
    readers_writers.write_resource(42, logger)
    expected_value = 42
    assert readers_writers._shared_resource == expected_value, "Shared resource not updated"
    assert readers_writers._is_writing is False, "Write lock not properly released"