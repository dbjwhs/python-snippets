# MIT License
# Copyright (c) 2025 dbjwhs

"""Implementation of specific pipeline stages."""

from pipeline.pipeline_stage import PipelineStage
from pipeline.safe_queue import SafeQueue
from pipeline.utils import Logger, sleep_ms


class MultiplyStage(PipelineStage[int]):
    """Multiplication stage that doubles input values."""

    def __init__(self, in_queue: SafeQueue[int], out_queue: SafeQueue[int], logger: Logger) -> None:
        """
        Initialize a new MultiplyStage instance.
        
        Args:
            in_queue: Queue for receiving input data
            out_queue: Queue for sending output data
            logger: Logger instance for logging
        """
        super().__init__(in_queue, out_queue, "Multiply Stage", logger)
    
    def process(self, item: int) -> None:
        """
        Implement multiplication processing.
        
        Args:
            item: The item to process
        """
        # Simulate processing time
        sleep_ms(100)
        self._output_queue.push(item * 2)


class AddStage(PipelineStage[int]):
    """Addition stage that adds 10 to input values."""

    def __init__(self, in_queue: SafeQueue[int], out_queue: SafeQueue[int], logger: Logger) -> None:
        """
        Initialize a new AddStage instance.
        
        Args:
            in_queue: Queue for receiving input data
            out_queue: Queue for sending output data
            logger: Logger instance for logging
        """
        super().__init__(in_queue, out_queue, "Add Stage", logger)
    
    def process(self, item: int) -> None:
        """
        Implement addition processing.
        
        Args:
            item: The item to process
        """
        # Simulate processing time
        sleep_ms(150)
        self._output_queue.push(item + 10)


class FilterStage(PipelineStage[int]):
    """Filter stage that only passes even numbers."""

    def __init__(self, in_queue: SafeQueue[int], out_queue: SafeQueue[int], logger: Logger) -> None:
        """
        Initialize a new FilterStage instance.
        
        Args:
            in_queue: Queue for receiving input data
            out_queue: Queue for sending output data
            logger: Logger instance for logging
        """
        super().__init__(in_queue, out_queue, "Filter Stage", logger)
    
    def process(self, item: int) -> None:
        """
        Implement filtering logic.
        
        Args:
            item: The item to process
        """
        # Simulate processing time
        sleep_ms(80)
        if item % 2 == 0:
            self._output_queue.push(item)