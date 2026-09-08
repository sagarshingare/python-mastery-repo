"""Run logging examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging
import tempfile
from pathlib import Path

from core_python.logging.debug_logging import log_scope, setup_logger, time_execution


def run_basic_logging() -> None:
    """Demonstrate basic structured logging setup."""
    print("\n--- Basic Logging ---")
    logger = setup_logger("demo.basic")
    logger.info("Application started")
    logger.warning("Low disk space detected")
    logger.error("Connection timeout to upstream service")
    print("(Check console output above)")


def run_file_logging() -> None:
    """Demonstrate logging to file."""
    print("\n--- File Logging ---")
    with tempfile.TemporaryDirectory() as tmp:
        log_file = Path(tmp) / "app.log"
        logger = setup_logger("demo.file", log_file=log_file)
        logger.info("This message goes to console AND file")
        logger.warning("Warning also logged to file")
        print(f"Log file contents:\n{log_file.read_text()}")


def run_log_scope() -> None:
    """Demonstrate scoped logging."""
    print("\n--- Log Scope ---")
    logger = setup_logger("demo.scope")
    with log_scope(logger, "data_processing"):
        logger.info("Processing batch 1 of 3")
        logger.info("Processing batch 2 of 3")
        logger.info("Processing batch 3 of 3")


def run_timed_function() -> None:
    """Demonstrate execution timing decorator."""
    print("\n--- Timed Function ---")

    @time_execution
    def slow_computation() -> int:
        """Simulate a slow computation."""
        total = 0
        for i in range(100_000):
            total += i
        return total

    result = slow_computation()
    print(f"Result: {result}")


def main() -> None:
    """Main entry point for logging examples."""
    parser = argparse.ArgumentParser(description="Run logging examples")
    parser.add_argument(
        "--module",
        choices=["basic", "file", "scope", "timed"],
        help="Specific example to run",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.module == "basic":
        run_basic_logging()
    elif args.module == "file":
        run_file_logging()
    elif args.module == "scope":
        run_log_scope()
    elif args.module == "timed":
        run_timed_function()
    else:
        run_basic_logging()
        run_file_logging()
        run_log_scope()
        run_timed_function()


if __name__ == "__main__":
    main()
