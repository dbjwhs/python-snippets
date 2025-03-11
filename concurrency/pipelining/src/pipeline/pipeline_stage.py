# MIT License
# Copyright (c) 2025 dbjwhs

"""Base class for pipeline stages that defines common functionality."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pipeline.safe_queue import SafeQueue
from pipeline.utils import Logger, LogLevel

T = TypeVar('T')


class PipelineStage(Generic[T], ABC):
    """Base class for pipeline stages that defines common functionality."""

    def __init__(
        self, 
        input_queue: SafeQueue[T], 
        output_queue: SafeQueue[T],
        stage_name: str,
        logger: Logger
    ) -> None:
        """
        Initialize a new pipeline stage.
        
        Args:
            input_queue: Queue for receiving input data
            output_queue: Queue for sending output data
            stage_name: Name identifier for the stage
            logger: Logger instance for logging
        """
        self._input_queue = input_queue
        self._output_queue = output_queue
        self._stage_name = stage_name
        self._logger = logger
    
    @abstractmethod
    def process(self, item: T) -> None:
        """
        Process a single item in the pipeline.
        
        This is a pure virtual function that must be implemented by subclasses
        to provide stage-specific processing.
        
        Args:
            item: The item to process
        """
    
    def run(self) -> None:
        """
        Main processing loop that handles input and output.
        
        This method runs in a loop, continuously processing items from the input
        queue and passing them to the process method until the input queue is
        empty and marked as done.
        """
        # Use a list with a placeholder as a container for the popped item
        item_container: list = [None]
        
        # Process items until the queue is empty and marked as done
        while self._input_queue.pop(item_container):
            # The actual item is now in item_container[0]
            item = item_container[0]
            self._logger.log(LogLevel.INFO, f"{self._stage_name} processing item: {item}")
            self.process(item)
        
        # Signal that no more items will be produced by this stage
        self._output_queue.set_done()