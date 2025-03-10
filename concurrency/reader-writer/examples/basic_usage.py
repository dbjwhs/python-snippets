# MIT License
# Copyright (c) 2025 dbjwhs

import time
from threading import Thread

from reader_writer.reader_writer import ReadersWriters
from reader_writer.utils import Logger, LogLevel, RandomGenerator


def basic_example() -> None:
    """
    Basic example demonstrating the ReadersWriters usage.
    
    This example creates 3 reader threads and 2 writer threads that
    concurrently access a shared resource.
    """
    logger = Logger.get_instance()
    logger.log(LogLevel.INFO, "Starting basic ReadersWriters example")
    
    # Create ReadersWriters instance
    rw = ReadersWriters()
    
    # Number of reader and writer threads
    reader_count = 3
    writer_count = 2
    
    # List to store all threads
    threads: list[Thread] = []
    
    # Create random number generator for operation counts
    random_gen = RandomGenerator(2, 5)
    
    # Create reader threads
    for i in range(reader_count):
        def reader_task(reader_id: int = i) -> None:
            logger.log(LogLevel.INFO, f"Reader {reader_id} started")
            # Perform a random number of read operations
            num_reads = random_gen.get_number()
            for _ in range(num_reads):
                rw.read_resource(logger)
                time.sleep(0.05)  # Small delay between reads
            logger.log(LogLevel.INFO, f"Reader {reader_id} finished after {num_reads} reads")
        
        thread = Thread(target=reader_task)
        threads.append(thread)
    
    # Create writer threads
    for i in range(writer_count):
        def writer_task(writer_id: int = i) -> None:
            logger.log(LogLevel.INFO, f"Writer {writer_id} started")
            # Perform a random number of write operations
            num_writes = random_gen.get_number()
            for write_idx in range(num_writes):
                value = writer_id * 100 + write_idx
                rw.write_resource(value, logger)
                time.sleep(0.1)  # Small delay between writes
            logger.log(LogLevel.INFO, f"Writer {writer_id} finished after {num_writes} writes")
        
        thread = Thread(target=writer_task)
        threads.append(thread)
    
    # Start all threads
    logger.log(LogLevel.INFO, f"Starting {len(threads)} threads")
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    logger.log(LogLevel.INFO, "All threads completed, example finished")


if __name__ == "__main__":
    basic_example()