# MIT License
# Copyright (c) 2025 dbjwhs

import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from threading import Event

from reader_writer.reader_writer import ReadersWriters
from reader_writer.utils import Logger, LogLevel, RandomGenerator


@dataclass
class SharedDatabase:
    """A shared database that will be protected by the ReadersWriters lock."""
    records: list[str] = field(default_factory=list)
    readers_writers: ReadersWriters = field(default_factory=ReadersWriters)
    logger: Logger = field(default_factory=Logger.get_instance)
    
    def add_record(self, record: str) -> None:
        """Add a record to the database (write operation)."""
        self.readers_writers.write_resource(len(self.records), self.logger)
        self.records.append(record)
        self.logger.log(LogLevel.INFO, f"Added record: {record}")
    
    def get_record(self, index: int) -> str | None:
        """Read a record from the database (read operation)."""
        self.readers_writers.read_resource(self.logger)
        if 0 <= index < len(self.records):
            record = self.records[index]
            self.logger.log(LogLevel.INFO, f"Read record at index {index}: {record}")
            return record
        self.logger.log(LogLevel.WARNING, f"Invalid record index: {index}")
        return None
    
    def get_record_count(self) -> int:
        """Get the number of records in the database (read operation)."""
        self.readers_writers.read_resource(self.logger)
        count = len(self.records)
        self.logger.log(LogLevel.INFO, f"Current record count: {count}")
        return count


def advanced_example() -> None:
    """
    Advanced example demonstrating ReadersWriters with a shared database.
    
    This example shows how to use ReadersWriters to protect a shared database
    with multiple readers and writers accessing it concurrently.
    """
    logger = Logger.get_instance()
    logger.log(LogLevel.INFO, "Starting advanced ReadersWriters example")
    
    # Create a shared database
    database = SharedDatabase()
    
    # Initialize with some data
    for i in range(5):
        database.add_record(f"Initial record {i}")
    
    # Number of reader and writer threads
    reader_count = 8
    writer_count = 3
    
    # Events to control thread execution
    start_event = Event()
    done_event = Event()
    
    # Random number generator for operation counts and delays
    random_gen = RandomGenerator(3, 10)
    
    # Writer function
    def writer_task(writer_id: int) -> None:
        logger.log(LogLevel.INFO, f"Writer {writer_id} waiting to start")
        start_event.wait()  # Wait for signal to start
        
        num_operations = random_gen.get_number()
        logger.log(LogLevel.INFO, f"Writer {writer_id} starting with {num_operations} operations")
        
        for i in range(num_operations):
            if done_event.is_set():
                break
                
            record = f"Record from writer {writer_id}, op {i}"
            database.add_record(record)
            
            # Random delay between operations
            time.sleep(random_gen.get_number() / 20)
        
        logger.log(LogLevel.INFO, f"Writer {writer_id} finished")
    
    # Reader function
    def reader_task(reader_id: int) -> None:
        logger.log(LogLevel.INFO, f"Reader {reader_id} waiting to start")
        start_event.wait()  # Wait for signal to start
        
        num_operations = random_gen.get_number()
        logger.log(LogLevel.INFO, f"Reader {reader_id} starting with {num_operations} operations")
        
        for i in range(num_operations):
            if done_event.is_set():
                break
                
            # Get current record count
            count = database.get_record_count()
            
            if count > 0:
                # Read a random record
                index = random_gen.get_number() % count
                record = database.get_record(index)
                logger.log(LogLevel.INFO, f"Reader {reader_id}, op {i}: Read record {index}: {record}")
            
            # Random delay between operations
            time.sleep(random_gen.get_number() / 30)
        
        logger.log(LogLevel.INFO, f"Reader {reader_id} finished")
    
    # Start all threads using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=reader_count + writer_count) as executor:
        # Submit reader tasks
        # The futures variables are stored in the executor and don't need to be tracked
        _ = [
            executor.submit(reader_task, i) for i in range(reader_count)
        ]
        
        # Submit writer tasks
        _ = [
            executor.submit(writer_task, i) for i in range(writer_count)
        ]
        
        # Give threads time to initialize
        time.sleep(0.5)
        
        # Signal all threads to start
        logger.log(LogLevel.INFO, "Signaling all threads to start")
        start_event.set()
        
        # Let threads run for a set time
        run_time = 3.0  # seconds
        logger.log(LogLevel.INFO, f"Running for {run_time} seconds")
        time.sleep(run_time)
        
        # Signal threads to finish
        logger.log(LogLevel.INFO, "Signaling threads to finish")
        done_event.set()
    
    # Print final database state
    logger.log(LogLevel.INFO, f"Final database has {database.get_record_count()} records")
    logger.log(LogLevel.INFO, "Advanced example completed")


if __name__ == "__main__":
    advanced_example()