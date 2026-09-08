"""Run Python iterator examples with a simple CLI."""

from __future__ import annotations
import argparse
import logging
from core_python.iterators.iterator_utils import (
    DatasetCollection,
    PeekableIterator,
    RangeIterator,
    group_consecutive,
    pairwise,
    read_until_sentinel,
    take,
)

logger = logging.getLogger(__name__)


def run_range_iterator_examples() -> None:
    """Demonstrate RangeIterator."""
    logger.info("Running RangeIterator examples")

    iterator = RangeIterator(0, 5, 1)
    print("RangeIterator(0, 5, 1):")
    for value in iterator:
        print(f"  Value: {value}")


def run_dataset_collection_examples() -> None:
    """Demonstrate Iterable vs Iterator (multi-pass and reversed)."""
    logger.info("Running DatasetCollection examples")

    dataset = DatasetCollection(["record_1", "record_2", "record_3"])
    print(f"Dataset length: {len(dataset)}")

    # First iteration
    print("Pass 1:", list(dataset))
    # Second iteration (doesn't exhaust!)
    print("Pass 2:", list(dataset))
    # Reversed iteration
    print("Reversed:", list(reversed(dataset)))


def run_sentinel_iterator_examples() -> None:
    """Demonstrate iter(callable, sentinel)."""
    logger.info("Running sentinel iterator examples")

    queue = [10, 20, 30, -1, 40]

    def pop_item():
        return queue.pop(0) if queue else -1

    # Read numbers until sentinel -1 is encountered
    items = read_until_sentinel(pop_item, -1)
    print(f"Read until sentinel -1: {items}")
    assert items == [10, 20, 30]


def run_traversal_examples() -> None:
    """Demonstrate take, pairwise, and group_consecutive."""
    logger.info("Running traversal helper examples")

    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"take(numbers, 4): {take(numbers, 4)}")
    print(f"pairwise(numbers[:5]): {list(pairwise(numbers[:5]))}")

    repeated = ["A", "A", "B", "C", "C", "C", "A"]
    print(f"group_consecutive({repeated}): {group_consecutive(repeated)}")


def run_peekable_iterator_examples() -> None:
    """Demonstrate PeekableIterator."""
    logger.info("Running PeekableIterator examples")

    items = ["first", "second", "third"]
    peekable = PeekableIterator(items)

    print(f"Peek: {peekable.peek()}")
    print(f"Next: {next(peekable)}")
    print(f"Peek: {peekable.peek()}")
    print(f"Next: {next(peekable)}")
    print(f"Next: {next(peekable)}")


def main() -> None:
    """Main entry point for running iterator examples."""
    parser = argparse.ArgumentParser(description="Run Python iterator examples")
    parser.add_argument(
        "--module",
        choices=["range", "dataset", "sentinel", "traversal", "peekable", "all"],
        default="all",
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "range":
        run_range_iterator_examples()
    elif args.module == "dataset":
        run_dataset_collection_examples()
    elif args.module == "sentinel":
        run_sentinel_iterator_examples()
    elif args.module == "traversal":
        run_traversal_examples()
    elif args.module == "peekable":
        run_peekable_iterator_examples()
    else:
        run_range_iterator_examples()
        run_dataset_collection_examples()
        run_sentinel_iterator_examples()
        run_traversal_examples()
        run_peekable_iterator_examples()


if __name__ == "__main__":
    main()
