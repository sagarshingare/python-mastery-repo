"""Run multithreading examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging

from core_python.multithreading.threading_examples import (
    ThreadSafeCounter,
    run_producer_consumer,
    simulate_io_tasks,
)

logger = logging.getLogger(__name__)


def run_thread_safe_counter() -> None:
    """Demonstrate thread-safe counter."""
    print("\n--- Thread-Safe Counter ---")
    counter = ThreadSafeCounter()
    import threading

    def worker() -> None:
        for _ in range(1000):
            counter.increment()

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Final counter: {counter.value} (expected 4000)")


def run_producer_consumer_demo() -> None:
    """Demonstrate producer-consumer pattern."""
    print("\n--- Producer-Consumer ---")
    result = run_producer_consumer(num_items=20, num_producers=2, num_consumers=3)
    print(f"Produced: {result.produced} | Consumed: {result.consumed} | Duration: {result.duration_seconds}s")


def run_io_simulation() -> None:
    """Demonstrate concurrent I/O tasks."""
    print("\n--- Simulated I/O Tasks ---")
    urls = [f"https://api.example.com/item/{i}" for i in range(8)]
    results = simulate_io_tasks(urls, delay=0.05, max_workers=4)
    for r in results:
        print(f"  {r['url']} → status={r['status']} thread={r['thread']}")


def main() -> None:
    """Main entry point for multithreading examples."""
    parser = argparse.ArgumentParser(description="Run multithreading examples")
    parser.add_argument(
        "--module",
        choices=["counter", "producer_consumer", "io_tasks"],
        help="Specific example to run",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.module == "counter":
        run_thread_safe_counter()
    elif args.module == "producer_consumer":
        run_producer_consumer_demo()
    elif args.module == "io_tasks":
        run_io_simulation()
    else:
        run_thread_safe_counter()
        run_producer_consumer_demo()
        run_io_simulation()


if __name__ == "__main__":
    main()
