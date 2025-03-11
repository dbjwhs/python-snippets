# MIT License
# Copyright (c) 2025 dbjwhs

"""
Example showing how to create custom pipeline stages.

This example demonstrates:
1. Creating custom pipeline stage classes
2. Processing more complex data types (strings)
3. Building a text processing pipeline
"""

import sys
import threading
import time
from typing import List
from dataclasses import dataclass

# Add project root to path
sys.path.append('/Users/dbjones/ng/dbjwhs/python-snippets/concurrency/pipelining')

from src.pipeline.safe_queue import SafeQueue
from src.pipeline.pipeline_stage import PipelineStage
from src.pipeline.utils import setup_logger, Logger


@dataclass
class TextItem:
    """Text item with ID and content for processing."""
    id: int
    content: str


class TextCleaningStage(PipelineStage[TextItem]):
    """Pipeline stage that cleans text by removing extra whitespace."""
    
    def __init__(self, in_queue: SafeQueue[TextItem], out_queue: SafeQueue[TextItem], logger: Logger) -> None:
        """Initialize the text cleaning stage."""
        super().__init__(in_queue, out_queue, "Text Cleaning Stage", logger)
    
    def process(self, item: TextItem) -> None:
        """Clean the text by removing extra whitespace."""
        # Simulate processing time
        time.sleep(0.1)
        
        # Clean the text: normalize whitespace and strip
        cleaned_text = " ".join(item.content.split())
        
        # Create a new text item with cleaned content
        self._output_queue.push(TextItem(item.id, cleaned_text))


class TextCapitalizationStage(PipelineStage[TextItem]):
    """Pipeline stage that capitalizes the first letter of each word."""
    
    def __init__(self, in_queue: SafeQueue[TextItem], out_queue: SafeQueue[TextItem], logger: Logger) -> None:
        """Initialize the text capitalization stage."""
        super().__init__(in_queue, out_queue, "Text Capitalization Stage", logger)
    
    def process(self, item: TextItem) -> None:
        """Capitalize the first letter of each word."""
        # Simulate processing time
        time.sleep(0.15)
        
        # Capitalize the first letter of each word
        capitalized_text = item.content.title()
        
        # Create a new text item with capitalized content
        self._output_queue.push(TextItem(item.id, capitalized_text))


class TextFilterStage(PipelineStage[TextItem]):
    """Pipeline stage that filters text items based on length."""
    
    def __init__(
        self, 
        in_queue: SafeQueue[TextItem], 
        out_queue: SafeQueue[TextItem], 
        min_length: int,
        logger: Logger
    ) -> None:
        """
        Initialize the text filter stage.
        
        Args:
            in_queue: Queue for receiving input data
            out_queue: Queue for sending output data
            min_length: Minimum length for text to pass the filter
            logger: Logger instance for logging
        """
        super().__init__(in_queue, out_queue, "Text Filter Stage", logger)
        self.min_length = min_length
    
    def process(self, item: TextItem) -> None:
        """Filter text items based on length."""
        # Simulate processing time
        time.sleep(0.08)
        
        # Only pass items that meet the minimum length requirement
        if len(item.content) >= self.min_length:
            self._output_queue.push(item)


def main() -> None:
    """Run the custom pipeline example."""
    # Initialize queues for each stage of the pipeline
    input_queue = SafeQueue[TextItem]()
    cleaning_queue = SafeQueue[TextItem]()
    capitalization_queue = SafeQueue[TextItem]()
    output_queue = SafeQueue[TextItem]()

    # Get the logger instance
    logger = setup_logger()
    logger.info("Starting custom text processing pipeline example")

    # Create pipeline stage objects
    cleaning_stage = TextCleaningStage(input_queue, cleaning_queue, logger)
    capitalization_stage = TextCapitalizationStage(cleaning_queue, capitalization_queue, logger)
    filter_stage = TextFilterStage(capitalization_queue, output_queue, 15, logger)
    
    # Create and start threads for each pipeline stage
    threads: List[threading.Thread] = []
    
    threads.append(threading.Thread(
        target=cleaning_stage.run, 
        name="Cleaning-Thread"
    ))
    
    threads.append(threading.Thread(
        target=capitalization_stage.run, 
        name="Capitalization-Thread"
    ))
    
    threads.append(threading.Thread(
        target=filter_stage.run, 
        name="Filter-Thread"
    ))
    
    # Start all processing threads
    for thread in threads:
        thread.start()
    
    # Sample text data
    sample_texts = [
        "  hello   world  ", 
        "this is a test", 
        "   pipeline  pattern   example   ",
        "short",
        "   concurrent   text    processing  with  python   ",
        "threads"
    ]
    
    # Feed sample data into the pipeline
    for i, text in enumerate(sample_texts):
        logger.info(f"Adding text {i+1}: '{text}'")
        input_queue.push(TextItem(i+1, text))
        time.sleep(0.2)  # Simulate data arrival rate
    
    # Signal that no more input data will be added
    input_queue.set_done()
    
    # Process output
    def process_output() -> None:
        logger.info("Starting to collect processed text")
        
        results: List[TextItem] = []
        item_container: list = [None]
        
        while output_queue.pop(item_container):
            item = item_container[0]
            results.append(TextItem(item.id, item.content))  # Create a copy
            logger.info(f"Processed text {item.id}: '{item.content}'")
        
        # Print summary
        logger.info(f"Text processing complete. {len(results)} items passed all stages.")
        
        # Print before and after comparison for all processed items
        if results:
            logger.info("\nBefore and After Comparison:")
            for result in results:
                original = sample_texts[result.id - 1]
                logger.info(f"ID {result.id}:")
                logger.info(f"  Before: '{original}'")
                logger.info(f"  After:  '{result.content}'")
    
    # Start output processing in a separate thread
    output_thread = threading.Thread(target=process_output, name="Output-Processor")
    output_thread.start()
    
    # Wait for all threads to complete
    for i, thread in enumerate(threads):
        thread.join()
        logger.info(f"Processing thread {i+1} completed")
    
    output_thread.join()
    logger.info("Pipeline processing complete!")


if __name__ == "__main__":
    main()