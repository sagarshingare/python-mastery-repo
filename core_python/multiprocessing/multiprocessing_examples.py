"""Multiprocessing examples for CPU-bound parallelism in Python."""

from __future__ import annotations

import logging
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Callable, Iterable

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProcessResult:
    """Result from a parallel computation.

    Attributes:
        worker_pid: Process ID of the worker that produced the result.
        input_value: The input that was processed.
        output_value: The computed output.
        duration_seconds: Wall-clock time taken by the worker.
    """

    worker_pid: int
    input_value: Any
    output_value: Any
    duration_seconds: float


# ---------------------------------------------------------------------------
# CPU-bound example functions
# ---------------------------------------------------------------------------

def _is_prime(n: int) -> bool:
    """Check whether *n* is a prime number (trial division)."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def count_primes_in_range(start: int, end: int) -> int:
    """Count the number of primes in ``[start, end)``."""
    return sum(1 for n in range(start, end) if _is_prime(n))


def compute_factorial_sum(n: int) -> int:
    """Compute the sum of factorials from ``1!`` to ``n!``.

    This is intentionally CPU-heavy to demonstrate multiprocessing benefits.
    """
    total = 0
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
        total += factorial
    return total


def _worker_wrapper(func: Callable[..., Any], args: tuple[Any, ...]) -> ProcessResult:
    """Thin wrapper that captures PID and timing for any worker function."""
    start = time.perf_counter()
    result = func(*args)
    duration = time.perf_counter() - start
    return ProcessResult(
        worker_pid=os.getpid(),
        input_value=args,
        output_value=result,
        duration_seconds=round(duration, 6),
    )


# ---------------------------------------------------------------------------
# High-level parallel utilities
# ---------------------------------------------------------------------------

def parallel_map(
    func: Callable[..., Any],
    items: Iterable[tuple[Any, ...]],
    *,
    max_workers: int | None = None,
) -> list[ProcessResult]:
    """Apply *func* to each item in *items* using a process pool.

    Args:
        func: A picklable function to execute in each worker.
        items: An iterable of argument tuples for *func*.
        max_workers: Maximum number of worker processes (defaults to CPU count).

    Returns:
        A list of :class:`ProcessResult` objects, one per input item.
    """
    max_workers = max_workers or multiprocessing.cpu_count()
    results: list[ProcessResult] = []

    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_worker_wrapper, func, args): args
            for args in items
        }
        for future in as_completed(futures):
            result = future.result()
            logger.info(
                "Worker PID=%d processed %s in %.4fs",
                result.worker_pid,
                result.input_value,
                result.duration_seconds,
            )
            results.append(result)

    return results


def parallel_prime_count(limit: int, chunk_size: int = 10_000) -> int:
    """Count primes up to *limit* by splitting work across processes.

    Args:
        limit: Upper bound (exclusive) for the prime search.
        chunk_size: Number of integers per worker chunk.

    Returns:
        Total number of primes found.
    """
    ranges = [
        (start, min(start + chunk_size, limit))
        for start in range(2, limit, chunk_size)
    ]
    results = parallel_map(count_primes_in_range, ranges)
    return sum(r.output_value for r in results)


class SharedCounterManager:
    """Demonstrate shared state between processes using ``multiprocessing.Value``.

    Attributes:
        counter: A shared integer counter.
        lock: A lock to protect concurrent counter updates.
    """

    def __init__(self) -> None:
        self.counter = multiprocessing.Value("i", 0)
        self.lock = multiprocessing.Lock()

    def increment(self, amount: int = 1) -> None:
        """Thread/process-safe increment."""
        with self.lock:
            self.counter.value += amount

    @property
    def value(self) -> int:
        """Current counter value."""
        return self.counter.value


def _increment_worker(counter: multiprocessing.Value, lock: multiprocessing.Lock, n: int) -> None:
    """Worker that increments a shared counter *n* times."""
    for _ in range(n):
        with lock:
            counter.value += 1


def demonstrate_shared_counter(num_processes: int = 4, increments_per_process: int = 1000) -> int:
    """Run multiple processes that increment a shared counter.

    Returns:
        Final counter value (should equal ``num_processes * increments_per_process``).
    """
    counter = multiprocessing.Value("i", 0)
    lock = multiprocessing.Lock()

    processes = [
        multiprocessing.Process(
            target=_increment_worker,
            args=(counter, lock, increments_per_process),
        )
        for _ in range(num_processes)
    ]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    return counter.value
