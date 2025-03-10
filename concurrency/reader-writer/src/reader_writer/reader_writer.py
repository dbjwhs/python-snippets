# MIT License
# Copyright (c) 2025 dbjwhs

import time
from threading import Condition, Lock, Thread
from typing import Final

from reader_writer.utils import Logger, LogLevel, NonCopyable, RandomGenerator, thread_id_to_string


class ReadersWriters:
    """
    Thread-safe implementation of the Readers-Writers synchronization pattern.
    
    This class allows multiple concurrent readers but only one writer at a time.
    Writers have priority over readers to prevent writer starvation.
    """
    
    def __init__(self) -> None:
        """Initialize the ReadersWriters instance."""
        # Resource protection
        self._mutex: Lock = Lock()
        self._read_cv: Condition = Condition(self._mutex)
        self._write_cv: Condition = Condition(self._mutex)
        
        # State tracking
        self._active_readers: int = 0
        self._waiting_readers: int = 0
        self._is_writing: bool = False
        self._waiting_writers: int = 0
        self._shared_resource: int = 0
    
    def start_read(self) -> None:
        """
        Acquire a read lock on the shared resource.
        
        This method will block if there's an active writer or waiting writers.
        """
        with self._mutex:
            # Increment waiting readers counter
            self._waiting_readers += 1
            
            # Wait if there's an active writer or waiting writers
            # This gives preference to writers to prevent their starvation
            while self._is_writing or self._waiting_writers > 0:
                self._read_cv.wait()
            
            # Decrement waiting readers and increment active readers
            self._waiting_readers -= 1
            self._active_readers += 1
    
    def end_read(self) -> None:
        """Release a read lock on the shared resource."""
        with self._mutex:
            # Decrement active readers count
            self._active_readers -= 1
            
            # If this was the last reader, notify a waiting writer
            if self._active_readers == 0:
                self._write_cv.notify()
    
    def start_write(self) -> None:
        """
        Acquire a write lock on the shared resource.
        
        This method will block until there are no active readers and no active writer.
        """
        with self._mutex:
            # Increment waiting writers counter
            self._waiting_writers += 1
            
            # Wait until there are no active readers and no active writer
            while self._is_writing or self._active_readers > 0:
                self._write_cv.wait()
            
            # Decrement waiting writers and set writing flag
            self._waiting_writers -= 1
            self._is_writing = True
    
    def end_write(self) -> None:
        """Release a write lock on the shared resource."""
        with self._mutex:
            # Clear writing flag
            self._is_writing = False
            
            # If there are waiting writers, give them priority
            # Otherwise, wake up all waiting readers
            if self._waiting_writers > 0:
                self._write_cv.notify()
            else:
                self._read_cv.notify_all()
    
    def read_resource(self, logger: Logger) -> None:
        """
        Read the shared resource with a RAII-style read lock.
        """
        class ReadLock(NonCopyable):
            """RAII wrapper for read lock acquisition and release."""
            
            def __init__(self, rw: ReadersWriters) -> None:
                """Acquire the read lock."""
                super().__init__()
                self._rw = rw
                self._rw.start_read()
                
            def __del__(self) -> None:
                """Release the read lock."""
                self._rw.end_read()
        
        # Create a read lock that automatically acquires and releases the lock
        _ = ReadLock(self)  # Variable keeps lock alive for method duration
        
        logger.log(LogLevel.INFO, f"Thread {thread_id_to_string()} reading resource: {self._shared_resource}")
        time.sleep(0.1)  # Simulate reading operation
    
    def write_resource(self, value: int, logger: Logger) -> None:
        """
        Write to the shared resource with a RAII-style write lock.
        """
        class WriteLock(NonCopyable):
            """RAII wrapper for write lock acquisition and release."""
            
            def __init__(self, rw: ReadersWriters) -> None:
                """Acquire the write lock."""
                super().__init__()
                self._rw = rw
                self._rw.start_write()
                
            def __del__(self) -> None:
                """Release the write lock."""
                self._rw.end_write()
        
        # Create a write lock that automatically acquires and releases the lock
        _ = WriteLock(self)  # Variable keeps lock alive for method duration
        
        self._shared_resource = value
        logger.log(LogLevel.INFO, f"Thread {thread_id_to_string()} wrote resource: {value}")
        time.sleep(0.2)  # Simulate writing operation


def main() -> None:
    """Run the example usage of ReadersWriters class."""
    logger = Logger.get_instance()
    
    # Setup how many reader/writer threads we want
    reader_thread_cnt: Final[int] = 2
    writer_thread_cnt: Final[int] = 5
    
    # Create a list to hold all threads
    threads: list[Thread] = []
    logger.log(LogLevel.INFO, f"Creating {reader_thread_cnt + writer_thread_cnt} threads")
    
    # Initialize readers-writers instance
    rw = ReadersWriters()
    
    # Generate random amounts of read/writes
    random_rw = RandomGenerator(3, 15)
    
    # Create reader threads
    for read_thrd_cnt in range(reader_thread_cnt):
        def reader_task(read_id: int = read_thrd_cnt) -> None:
            """Reader thread task."""
            logger.log(LogLevel.INFO, f"Started reader thread {read_id}")
            read_cnt = random_rw.get_number()
            for _ in range(read_cnt):
                rw.read_resource(logger)
                time.sleep(0.05)
            logger.log(LogLevel.INFO, f"Finished reader thread {read_id}")
        
        thread = Thread(target=reader_task)
        threads.append(thread)
    
    # Create writer threads
    for write_thrd_cnt in range(writer_thread_cnt):
        def writer_task(write_id: int = write_thrd_cnt) -> None:
            """Writer thread task."""
            logger.log(LogLevel.INFO, f"Started writer thread {write_id}")
            write_cnt = random_rw.get_number()
            for writes in range(write_cnt):
                rw.write_resource(write_id * 10 + writes, logger)
                time.sleep(0.1)
            logger.log(LogLevel.INFO, f"Finished writer thread {write_id}")
        
        thread = Thread(target=writer_task)
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()