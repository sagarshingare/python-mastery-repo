"""Run Python generator examples with a simple CLI."""

from __future__ import annotations
import argparse
import logging
from core_python.generators.generator_examples import (
    chunked_generator,
    fibonacci_generator,
    filter_generator,
    flatten_nested,
    normalized_strings,
    run_pipeline,
    running_average,
)

logger = logging.getLogger(__name__)


def run_basic_examples() -> None:
    """Demonstrate basic generator functions."""
    logger.info("Running basic generator examples")

    print("Fibonacci numbers <= 20:")
    for num in fibonacci_generator(20):
        print(f"  {num}")

    print("\nChunked generator:")
    data = list(range(10))
    for chunk in chunked_generator(data, 3):
        print(f"  Chunk: {chunk}")

    print("\nFilter generator (even numbers):")
    evens = filter_generator(range(10), lambda x: x % 2 == 0)
    print(f"  Evens: {list(evens)}")

    print("\nNormalized strings:")
    raw = ["  Hello  ", "WORLD\n", "\ttEsT  "]
    print(f"  Clean: {list(normalized_strings(raw))}")


def run_flatten_and_coroutine_examples() -> None:
    """Demonstrate yield from recursion and coroutine two-way communication."""
    logger.info("Running flatten and coroutine examples")

    # 1. Recursive yield from
    nested = [1, [2, [3, 4], 5], [[6]], 7]
    flattened = list(flatten_nested(nested))
    print(f"Nested {nested} -> Flattened: {flattened}")
    assert flattened == [1, 2, 3, 4, 5, 6, 7]

    # 2. Coroutine send / running average
    avg_gen = running_average()
    next(avg_gen)  # Prime the generator to first yield
    print("Running average coroutine:")
    print("  Sent 10 -> Avg:", avg_gen.send(10))
    print("  Sent 20 -> Avg:", avg_gen.send(20))
    print("  Sent 30 -> Avg:", avg_gen.send(30))
    avg_gen.close()


def run_streaming_pipeline_examples() -> None:
    """Demonstrate memory-efficient multi-stage pipeline."""
    logger.info("Running streaming pipeline examples")
    results = run_pipeline(6)
    print(f"Pipeline processed {len(results)} events:")
    for r in results:
        print(f"  Event #{r['id']}: amount={r['amount']}, total_with_tax={r['total_with_tax']}")


def main() -> None:
    """Main entry point for running examples."""
    parser = argparse.ArgumentParser(description="Run Python generator examples")
    parser.add_argument(
        "--module",
        choices=["basic", "coroutine", "pipeline", "all"],
        default="all",
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "basic":
        run_basic_examples()
    elif args.module == "coroutine":
        run_flatten_and_coroutine_examples()
    elif args.module == "pipeline":
        run_streaming_pipeline_examples()
    else:
        run_basic_examples()
        run_flatten_and_coroutine_examples()
        run_streaming_pipeline_examples()


if __name__ == "__main__":
    main()