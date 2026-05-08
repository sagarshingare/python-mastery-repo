"""Run Python decorator examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging
import random
import time
from pathlib import Path

from core_python.decorators.decorators import (
    memoize,
    retry,
    timer,
    validate_non_empty_string,
)

logger = logging.getLogger(__name__)


def run_timer_examples() -> None:
    """Demonstrate the timer decorator."""
    logger.info("Running timer decorator examples")

    @timer
    def slow_function(seconds: float) -> str:
        """A function that simulates slow execution."""
        time.sleep(seconds)
        return f"Slept for {seconds} seconds"

    print("slow_function(0.1) ->", slow_function(0.1))
    print("slow_function(0.2) ->", slow_function(0.2))


def run_retry_examples() -> None:
    """Demonstrate the retry decorator."""
    logger.info("Running retry decorator examples")

    @retry(max_attempts=3, delay_seconds=0.1)
    def unreliable_function() -> str:
        """A function that fails randomly."""
        if random.random() < 0.7:  # 70% chance to fail
            raise ValueError("Random failure")
        return "Success!"

    print("unreliable_function() ->", unreliable_function())


def run_memoize_examples() -> None:
    """Demonstrate the memoize decorator."""
    logger.info("Running memoize decorator examples")

    @memoize
    def expensive_computation(n: int) -> int:
        """Simulate an expensive computation."""
        time.sleep(0.1)  # Simulate delay
        return n * n

    print("expensive_computation(5) ->", expensive_computation(5))
    print("expensive_computation(5) ->", expensive_computation(5))  # Should be cached
    print("expensive_computation(10) ->", expensive_computation(10))


def run_validate_examples() -> None:
    """Demonstrate the validate_non_empty_string decorator."""
    logger.info("Running validate_non_empty_string decorator examples")

    @validate_non_empty_string
    def process_string(value: str) -> str:
        """Process a non-empty string."""
        return f"Processed: {value.upper()}"

    try:
        print("process_string('hello') ->", process_string("hello"))
    except ValueError as e:
        print(f"Error: {e}")

    try:
        print("process_string('') ->", process_string(""))
    except ValueError as e:
        print(f"Error: {e}")


def main() -> None:
    """Main entry point for running examples."""
    parser = argparse.ArgumentParser(description="Run Python decorator examples")
    parser.add_argument(
        "--module",
        choices=["timer", "retry", "memoize", "validate"],
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "timer":
        run_timer_examples()
    elif args.module == "retry":
        run_retry_examples()
    elif args.module == "memoize":
        run_memoize_examples()
    elif args.module == "validate":
        run_validate_examples()
    else:
        # Run all examples
        run_timer_examples()
        run_retry_examples()
        run_memoize_examples()
        run_validate_examples()


if __name__ == "__main__":
    main()