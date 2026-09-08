"""Run multiprocessing examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging
import time

from core_python.multiprocessing.multiprocessing_examples import (
    compute_factorial_sum,
    count_primes_in_range,
    demonstrate_shared_counter,
    parallel_map,
    parallel_prime_count,
)

logger = logging.getLogger(__name__)


def run_prime_count() -> None:
    """Demonstrate parallel prime counting."""
    limit = 100_000
    print(f"\n--- Parallel Prime Count (up to {limit:,}) ---")

    start = time.perf_counter()
    count = parallel_prime_count(limit, chunk_size=10_000)
    duration = time.perf_counter() - start

    print(f"Found {count:,} primes in {duration:.3f}s")


def run_parallel_map() -> None:
    """Demonstrate parallel_map with factorial computation."""
    print("\n--- Parallel Map (Factorial Sums) ---")
    items = [(n,) for n in [100, 200, 300, 400, 500]]
    results = parallel_map(compute_factorial_sum, items, max_workers=2)

    for r in sorted(results, key=lambda x: x.input_value):
        print(f"  Input={r.input_value} | PID={r.worker_pid} | Duration={r.duration_seconds}s")


def run_shared_counter() -> None:
    """Demonstrate shared counter across processes."""
    print("\n--- Shared Counter ---")
    num_procs = 4
    increments = 500
    final = demonstrate_shared_counter(num_procs, increments)
    expected = num_procs * increments
    print(f"Final counter: {final} (expected {expected}) — {'OK' if final == expected else 'MISMATCH'}")


def main() -> None:
    """Main entry point for multiprocessing examples."""
    parser = argparse.ArgumentParser(description="Run multiprocessing examples")
    parser.add_argument(
        "--module",
        choices=["primes", "parallel_map", "shared_counter"],
        help="Specific example to run",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.module == "primes":
        run_prime_count()
    elif args.module == "parallel_map":
        run_parallel_map()
    elif args.module == "shared_counter":
        run_shared_counter()
    else:
        run_prime_count()
        run_parallel_map()
        run_shared_counter()


if __name__ == "__main__":
    main()
