"""Run Python generator examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from core_python.generators.generator_examples import (
    chunked_generator,
    fibonacci_generator,
    filter_generator,
    normalized_strings,
)

logger = logging.getLogger(__name__)


def run_fibonacci_examples() -> None:
    """Demonstrate fibonacci generator."""
    logger.info("Running fibonacci generator examples")

    print("Fibonacci numbers up to 50:")
    fib_gen = fibonacci_generator(50)
    print(list(fib_gen))


def run_chunked_examples() -> None:
    """Demonstrate chunked generator."""
    logger.info("Running chunked generator examples")

    data = list(range(1, 11))  # [1, 2, 3, ..., 10]
    print(f"Original data: {data}")
    print("Chunked into groups of 3:")
    for chunk in chunked_generator(data, 3):
        print(chunk)


def run_filter_examples() -> None:
    """Demonstrate filter generator."""
    logger.info("Running filter generator examples")

    numbers = list(range(1, 21))  # [1, 2, ..., 20]
    print(f"Original numbers: {numbers}")
    print("Even numbers only:")
    even_gen = filter_generator(numbers, lambda x: x % 2 == 0)
    print(list(even_gen))


def run_normalized_strings_examples() -> None:
    """Demonstrate normalized strings generator."""
    logger.info("Running normalized strings examples")

    messy_strings = ["  Hello  ", "WORLD", "  python  ", "GeNeRaToRs"]
    print(f"Original strings: {messy_strings}")
    print("Normalized strings:")
    normalized_gen = normalized_strings(messy_strings)
    print(list(normalized_gen))


def main() -> None:
    """Main entry point for running examples."""
    parser = argparse.ArgumentParser(description="Run Python generator examples")
    parser.add_argument(
        "--module",
        choices=["fibonacci", "chunked", "filter", "normalized"],
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "fibonacci":
        run_fibonacci_examples()
    elif args.module == "chunked":
        run_chunked_examples()
    elif args.module == "filter":
        run_filter_examples()
    elif args.module == "normalized":
        run_normalized_strings_examples()
    else:
        # Run all examples
        run_fibonacci_examples()
        run_chunked_examples()
        run_filter_examples()
        run_normalized_strings_examples()


if __name__ == "__main__":
    main()