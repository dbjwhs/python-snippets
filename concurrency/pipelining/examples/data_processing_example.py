# MIT License
# Copyright (c) 2025 dbjwhs

"""
Example showing how to use the pipeline pattern for data processing.

This example demonstrates a data processing pipeline with the following stages:
1. Data generation (generator function)
2. Multiplication (doubles each value)
3. Addition (adds 10 to each value)
4. Filtering (keeps only even values)
5. Output (prints the results)
"""

import sys
import threading
import time
from typing import List

# Add project root to path
sys.path.append('/Users/dbjones/ng/dbjwhs/python-snippets/concurrency/pipelining')

from src.pipeline.safe_queue import SafeQueue
from src.pipeline.stages import MultiplyStage, AddStage, FilterStage
from src.pipeline.utils import setup_logger


def main() -> None:
    """Run the data processing example."""
    # Initialize queues for each stage of the pipeline
    input_queue = SafeQueue[int]()
    multiply_queue = SafeQueue[int]()
    add_queue = SafeQueue[int]()
    output_queue = SafeQueue[int]()

    # Get the logger instance
    logger = setup_logger()
    logger.info("Starting data processing pipeline example")

    # Create pipeline stage objects
    multiply_stage = MultiplyStage(input_queue, multiply_queue, logger)
    add_stage = AddStage(multiply_queue, add_queue, logger)
    filter_stage = FilterStage(add_queue, output_queue, logger)
    
    # Create and start threads for each pipeline stage
    threads: List[threading.Thread] = []
    
    threads.append(threading.Thread(
        target=multiply_stage.run, 
        name="Multiply-Thread"
    ))
    
    threads.append(threading.Thread(
        target=add_stage.run, 
        name="Add-Thread"
    ))
    
    threads.append(threading.Thread(
        target=filter_stage.run, 
        name="Filter-Thread"
    ))
    
    # Start all processing threads
    for thread in threads:
        thread.start()
    
    # Data generator function - simulates data source
    def generate_data() -> None:
        logger.info("Generating input data")
        for i in range(1, 21):  # Generate 20 items
            logger.info(f"Generating item: {i}")
            input_queue.push(i)
            time.sleep(0.1)  # Simulate data arrival rate
        
        logger.info("Data generation complete")
        input_queue.set_done()
    
    # Start data generator in a separate thread
    data_thread = threading.Thread(target=generate_data, name="Data-Generator")
    data_thread.start()
    
    # Output consumer function - collects and displays results
    def consume_output() -> None:
        total_count = 0
        sum_value = 0
        
        logger.info("Starting to collect results")
        item_container: list = [None]
        while output_queue.pop(item_container):
            item = item_container[0]
            total_count += 1
            sum_value += item
            logger.info(f"Received result: {item}")
        
        # Print summary statistics
        logger.info(f"Processing complete. Received {total_count} items.")
        if total_count > 0:
            logger.info(f"Average value: {sum_value / total_count:.2f}")
    
    # Start output consumer in a separate thread
    output_thread = threading.Thread(target=consume_output, name="Output-Consumer")
    output_thread.start()
    
    # Wait for all threads to complete
    data_thread.join()
    logger.info("Data generation thread completed")
    
    for i, thread in enumerate(threads):
        thread.join()
        logger.info(f"Processing thread {i+1} completed")
    
    output_thread.join()
    logger.info("Output consumer thread completed")
    
    logger.info("Pipeline processing complete!")


if __name__ == "__main__":
    main()