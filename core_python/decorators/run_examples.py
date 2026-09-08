"""Run Python decorator examples with a simple CLI."""

from __future__ import annotations
import argparse
import logging
import time
from core_python.decorators.decorators import (
    CallCounter,
    audit_log,
    memoize,
    repeat,
    retry,
    singleton_class,
    timer,
    validate_non_empty_string,
)

logger = logging.getLogger(__name__)


def run_timer_examples() -> None:
    """Demonstrate the timer decorator."""
    logger.info("Running timer decorator examples")

    @timer
    def slow_function(seconds: float) -> str:
        """A function that simulates execution time."""
        time.sleep(seconds)
        return f"Slept for {seconds} seconds"

    print("slow_function(0.05) ->", slow_function(0.05))


def run_retry_examples() -> None:
    """Demonstrate the retry decorator deterministically."""
    logger.info("Running retry decorator examples")

    attempt_counter = 0

    @retry(max_attempts=3, delay_seconds=0.01)
    def flaky_service() -> str:
        """Fails on first 2 calls, succeeds on 3rd."""
        nonlocal attempt_counter
        attempt_counter += 1
        if attempt_counter < 3:
            raise ConnectionError(f"Transient connection error on attempt {attempt_counter}")
        return "Connected to upstream service!"

    print("flaky_service() ->", flaky_service())

    # Exhaustion check
    @retry(max_attempts=2, delay_seconds=0.01)
    def failing_service() -> None:
        raise ValueError("Permanent fatal failure")

    try:
        failing_service()
    except ValueError as err:
        print(f"Caught expected exhaustion error: {err}")


def run_memoize_examples() -> None:
    """Demonstrate the memoize decorator."""
    logger.info("Running memoize decorator examples")

    @memoize
    def expensive_computation(n: int) -> int:
        """Simulate an expensive computation."""
        return n * n

    print("expensive_computation(5) ->", expensive_computation(5))
    print("expensive_computation(5) ->", expensive_computation(5))  # Cached
    print("expensive_computation(10) ->", expensive_computation(10))


def run_validate_examples() -> None:
    """Demonstrate the validate_non_empty_string decorator."""
    logger.info("Running validate_non_empty_string decorator examples")

    @validate_non_empty_string
    def process_string(value: str) -> str:
        return f"Processed: {value.upper()}"

    print("process_string('hello') ->", process_string("hello"))
    try:
        process_string("")
    except ValueError as e:
        print(f"Caught expected validation error: {e}")


def run_stateful_and_dual_examples() -> None:
    """Demonstrate stateful class decorator and dual-use decorator."""
    logger.info("Running stateful and dual-use decorator examples")

    # 1. Stateful CallCounter
    @CallCounter
    def compute_hash(text: str) -> str:
        return f"hash_{hash(text) % 1000}"

    compute_hash("apple")
    compute_hash("banana")
    compute_hash("cherry")
    print(f"compute_hash call count: {compute_hash.call_count}")

    # 2. Dual-use @audit_log
    @audit_log
    def bare_logged() -> str:
        return "bare ok"

    @audit_log(action="EXPORT_PDF")
    def parameterized_logged() -> str:
        return "param ok"

    print(f"bare_logged() -> {bare_logged()}")
    print(f"parameterized_logged() -> {parameterized_logged()}")


def run_class_decorator_examples() -> None:
    """Demonstrate class-level singleton decorator."""
    logger.info("Running class decorator examples")

    @singleton_class
    class DatabaseConnectionPool:
        def __init__(self) -> None:
            self.created_at = time.time()

    pool1 = DatabaseConnectionPool()
    pool2 = DatabaseConnectionPool()
    print(f"pool1 is pool2 (singleton): {pool1 is pool2}")
    assert pool1 is pool2


def main() -> None:
    """Main entry point for running decorator examples."""
    parser = argparse.ArgumentParser(description="Run Python decorator examples")
    parser.add_argument(
        "--module",
        choices=["timer", "retry", "memoize", "validate", "stateful", "class_dec", "all"],
        default="all",
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

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
    elif args.module == "stateful":
        run_stateful_and_dual_examples()
    elif args.module == "class_dec":
        run_class_decorator_examples()
    else:
        run_timer_examples()
        run_retry_examples()
        run_memoize_examples()
        run_validate_examples()
        run_stateful_and_dual_examples()
        run_class_decorator_examples()


if __name__ == "__main__":
    main()