# MIT License
# Copyright (c) 2025 dbjwhs

"""Main module for the pipeline package."""

import threading

from icecream import ic

from pipeline.safe_queue import SafeQueue
from pipeline.stages import AddStage, FilterStage, MultiplyStage
from pipeline.utils import setup_logger


def main() -> None:
    """Run the pipeline example."""
    # Configure icecream for logging
    ic.configureOutput(prefix='')
    
    # Initialize queues for each stage of the pipeline
    input_queue = SafeQueue[int]()
    multiply_queue = SafeQueue[int]()
    add_queue = SafeQueue[int]()
    output_queue = SafeQueue[int]()

    # Get the logger instance
    logger = setup_logger()

    # Create pipeline stage objects
    multiply_stage = MultiplyStage(input_queue, multiply_queue, logger)
    add_stage = AddStage(multiply_queue, add_queue, logger)
    filter_stage = FilterStage(add_queue, output_queue, logger)

    # Create and start threads for each pipeline stage
    multiply_thread = threading.Thread(target=multiply_stage.run)
    add_thread = threading.Thread(target=add_stage.run)
    filter_thread = threading.Thread(target=filter_stage.run)

    # Start all processing threads
    multiply_thread.start()
    add_thread.start()
    filter_thread.start()

    # Feed input data into the pipeline
    for i in range(1, 11):
        input_queue.push(i)
    
    # Signal that no more input data will be added
    input_queue.set_done()

    # Create output processing thread
    def process_output() -> None:
        item_container: list = [None]
        while output_queue.pop(item_container):
            item = item_container[0]
            logger.info(f"Final output: {item}")

    output_thread = threading.Thread(target=process_output)
    output_thread.start()

    # Wait for all pipeline stages to complete
    multiply_thread.join()
    add_thread.join()
    filter_thread.join()
    output_thread.join()


if __name__ == "__main__":
    main()