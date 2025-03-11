# MIT License
# Copyright (c) 2025 dbjwhs

"""Tests for the pipeline stages."""

import threading
import time
import pytest
from typing import List

import sys
sys.path.append('/Users/dbjones/ng/dbjwhs/python-snippets/concurrency/pipelining')
from src.pipeline.safe_queue import SafeQueue
from src.pipeline.stages import MultiplyStage, AddStage, FilterStage


def test_multiply_stage(logger) -> None:
    """Test the MultiplyStage."""
    # Set up the input and output queues
    input_queue: SafeQueue[int] = SafeQueue()
    output_queue: SafeQueue[int] = SafeQueue()
    
    # Create the stage
    stage = MultiplyStage(input_queue, output_queue, logger)
    
    # Set up a thread to run the stage
    thread = threading.Thread(target=stage.run)
    thread.start()
    
    # Push some values
    input_queue.push(1)
    input_queue.push(2)
    input_queue.push(3)
    input_queue.set_done()
    
    # Get the results
    results: List[int] = []
    val_container: list = [None]
    while output_queue.pop(val_container):
        results.append(val_container[0])
    
    # Wait for the thread to finish
    thread.join()
    
    # Check the results
    assert sorted(results) == [2, 4, 6]


def test_add_stage(logger) -> None:
    """Test the AddStage."""
    # Set up the input and output queues
    input_queue: SafeQueue[int] = SafeQueue()
    output_queue: SafeQueue[int] = SafeQueue()
    
    # Create the stage
    stage = AddStage(input_queue, output_queue, logger)
    
    # Set up a thread to run the stage
    thread = threading.Thread(target=stage.run)
    thread.start()
    
    # Push some values
    input_queue.push(1)
    input_queue.push(2)
    input_queue.push(3)
    input_queue.set_done()
    
    # Get the results
    results: List[int] = []
    val_container: list = [None]
    while output_queue.pop(val_container):
        results.append(val_container[0])
    
    # Wait for the thread to finish
    thread.join()
    
    # Check the results
    assert sorted(results) == [11, 12, 13]


def test_filter_stage(logger) -> None:
    """Test the FilterStage."""
    # Set up the input and output queues
    input_queue: SafeQueue[int] = SafeQueue()
    output_queue: SafeQueue[int] = SafeQueue()
    
    # Create the stage
    stage = FilterStage(input_queue, output_queue, logger)
    
    # Set up a thread to run the stage
    thread = threading.Thread(target=stage.run)
    thread.start()
    
    # Push some values
    input_queue.push(1)
    input_queue.push(2)
    input_queue.push(3)
    input_queue.push(4)
    input_queue.set_done()
    
    # Get the results
    results: List[int] = []
    val_container: list = [None]
    while output_queue.pop(val_container):
        results.append(val_container[0])
    
    # Wait for the thread to finish
    thread.join()
    
    # Check the results (only even numbers should be included)
    assert sorted(results) == [2, 4]


def test_pipeline_integration(logger) -> None:
    """Test the full pipeline integration."""
    # Set up the queues
    input_queue: SafeQueue[int] = SafeQueue()
    multiply_queue: SafeQueue[int] = SafeQueue()
    add_queue: SafeQueue[int] = SafeQueue()
    output_queue: SafeQueue[int] = SafeQueue()
    
    # Create the stages
    multiply_stage = MultiplyStage(input_queue, multiply_queue, logger)
    add_stage = AddStage(multiply_queue, add_queue, logger)
    filter_stage = FilterStage(add_queue, output_queue, logger)
    
    # Create and start the threads
    multiply_thread = threading.Thread(target=multiply_stage.run)
    add_thread = threading.Thread(target=add_stage.run)
    filter_thread = threading.Thread(target=filter_stage.run)
    
    multiply_thread.start()
    add_thread.start()
    filter_thread.start()
    
    # Push input values
    for i in range(1, 6):
        input_queue.push(i)
    input_queue.set_done()
    
    # Get the results
    results: List[int] = []
    val_container: list = [None]
    while output_queue.pop(val_container):
        results.append(val_container[0])
    
    # Wait for all threads to finish
    multiply_thread.join()
    add_thread.join()
    filter_thread.join()
    
    # Check the pipeline results:
    # 1. Multiply by 2: [2, 4, 6, 8, 10]
    # 2. Add 10: [12, 14, 16, 18, 20]
    # 3. Filter even: [12, 14, 16, 18, 20] (all are even)
    assert sorted(results) == [12, 14, 16, 18, 20]