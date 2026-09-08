"""Run memory management and profiling examples with a simple CLI."""

from __future__ import annotations
import argparse
import logging
from core_python.memory_management.memory_utils import (
    ExpensivePayload,
    WeakCache,
    analyze_memory,
    compare_slots_vs_dict,
    create_circular_reference_and_collect,
    get_reference_count,
    get_size,
)

logger = logging.getLogger(__name__)


def run_sizing_examples() -> None:
    """Demonstrate object memory sizing."""
    logger.info("Running memory sizing examples")

    small_list = [1, 2, 3]
    nested_list = [1, [2, 3], {"key": "value"}]

    print(f"sys.getsizeof([1, 2, 3]): {get_size(small_list)} bytes")
    print(f"Deep size of nested list: {get_size(nested_list, deep=True)} bytes")

    report = analyze_memory(nested_list)
    print(f"MemoryReport: type={report.object_type}, shallow={report.shallow_size}, deep={report.deep_size}")


def run_refcount_and_cycles() -> None:
    """Demonstrate reference counting and circular cycle garbage collection."""
    logger.info("Running reference count & cycles examples")

    sample = ["mastery"]
    initial_refs = get_reference_count(sample)
    print(f"Initial reference count of sample: {initial_refs}")

    alias_1 = sample
    alias_2 = sample
    print(f"Reference count with 2 extra aliases: {get_reference_count(sample)}")
    assert get_reference_count(sample) == initial_refs + 2

    del alias_1, alias_2
    print(f"Reference count after deleting aliases: {get_reference_count(sample)}")

    # Circular reference collection
    collected = create_circular_reference_and_collect()
    print(f"gc.collect() successfully reaped {collected} objects from circular reference cycle.")


def run_weakref_examples() -> None:
    """Demonstrate weakref cache behavior."""
    logger.info("Running weak reference cache examples")

    cache = WeakCache()
    item1 = ExpensivePayload("user_profile_1")
    item2 = ExpensivePayload("user_profile_2")

    cache.set("item1", item1)
    cache.set("item2", item2)
    print(f"Cache size with strong references active: {cache.size()}")
    assert cache.size() == 2

    # Drop strong reference to item1
    del item1
    print(f"Cache size after deleting strong reference to item1: {cache.size()}")
    assert cache.size() == 1
    assert cache.get("item1") is None
    assert cache.get("item2") is not None


def run_slots_benchmark() -> None:
    """Demonstrate memory savings of __slots__ vs __dict__."""
    logger.info("Running __slots__ vs __dict__ memory comparison")
    results = compare_slots_vs_dict(20000)
    print(f"Allocated {results['count']} instances:")
    print(f"  Standard __dict__ peak memory: {results['regular_peak_bytes']:,} bytes")
    print(f"  Slotted __slots__ peak memory: {results['slotted_peak_bytes']:,} bytes")
    print(f"  Memory saved: {results['memory_saved_percent']}%")


def main() -> None:
    """Main entry point for running memory examples."""
    parser = argparse.ArgumentParser(description="Run Python memory management examples")
    parser.add_argument(
        "--module",
        choices=["sizing", "refcount", "weakref", "slots", "all"],
        default="all",
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.module == "sizing":
        run_sizing_examples()
    elif args.module == "refcount":
        run_refcount_and_cycles()
    elif args.module == "weakref":
        run_weakref_examples()
    elif args.module == "slots":
        run_slots_benchmark()
    else:
        run_sizing_examples()
        run_refcount_and_cycles()
        run_weakref_examples()
        run_slots_benchmark()


if __name__ == "__main__":
    main()
