"""Main entry point for the barrier example package."""

from barrier_example.examples import CustomBarrierExample, IceCreamLogger, ModernBarrierExample


def main() -> None:
    """Run the barrier example demonstrations."""
    # Constants
    num_threads = 4

    # Thread-safe logger
    logger = IceCreamLogger()

    # Demonstrate both implementations
    CustomBarrierExample.demonstrate(num_threads, logger)
    logger.log("\n-----------------------------------")
    ModernBarrierExample.demonstrate(num_threads, logger)


if __name__ == "__main__":
    main()
