"""
Main entry point for the producer_consumer package.

This module runs the producer-consumer demo when the package is executed
as a module: `python -m producer_consumer`
"""

from icecream import ic

# Handle both installed package and development imports
try:
    from producer_consumer.producer_consumer import run_producer_consumer_demo
except ImportError:
    from .producer_consumer import run_producer_consumer_demo

if __name__ == "__main__":
    ic.configureOutput(prefix="[Producer-Consumer] ")
    ic("Starting producer-consumer demonstration")
    run_producer_consumer_demo()