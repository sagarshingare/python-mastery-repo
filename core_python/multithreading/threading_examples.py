"""Multithreading examples for I/O-bound concurrency in Python."""

from __future__ import annotations

import logging
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Thread-safe data structures
# ---------------------------------------------------------------------------

class ThreadSafeCounter:
    """A counter that can be safely incremented from multiple threads.

    Uses a ``threading.Lock`` to protect the internal value.
    """

    def __init__(self, initial: int = 0) -> None:
        self._value = initial
        self._lock = threading.Lock()

    def increment(self, amount: int = 1) -> None:
        """Atomically increment the counter."""
        with self._lock:
            self._value += amount

    def decrement(self, amount: int = 1) -> None:
        """Atomically decrement the counter."""
        with self._lock:
            self._value -= amount

    @property
    def value(self) -> int:
        """Current counter value."""
        with self._lock:
            return self._value


class BoundedBuffer:
    """A thread-safe bounded buffer implementing the producer-consumer pattern.

    Uses ``queue.Queue`` which is internally synchronised.
    """

    def __init__(self, capacity: int = 10) -> None:
        self._queue: queue.Queue[Any] = queue.Queue(maxsize=capacity)

    def put(self, item: Any, timeout: float | None = None) -> None:
        """Add an item to the buffer (blocks if full)."""
        self._queue.put(item, timeout=timeout)

    def get(self, timeout: float | None = None) -> Any:
        """Remove and return an item from the buffer (blocks if empty)."""
        return self._queue.get(timeout=timeout)

    def task_done(self) -> None:
        """Signal that a consumed item has been fully processed."""
        self._queue.task_done()

    def join(self) -> None:
        """Block until all items have been processed."""
        self._queue.join()

    @property
    def size(self) -> int:
        """Approximate current size of the buffer."""
        return self._queue.qsize()


# ---------------------------------------------------------------------------
# Producer-consumer demonstration
# ---------------------------------------------------------------------------

@dataclass
class ProducerConsumerResult:
    """Summary produced after a producer-consumer run."""

    produced: int = 0
    consumed: int = 0
    duration_seconds: float = 0.0


def run_producer_consumer(
    num_items: int = 20,
    num_producers: int = 2,
    num_consumers: int = 3,
    buffer_capacity: int = 5,
) -> ProducerConsumerResult:
    """Run a producer-consumer pipeline with multiple threads.

    Args:
        num_items: Total items to produce.
        num_producers: Number of producer threads.
        num_consumers: Number of consumer threads.
        buffer_capacity: Maximum items in the shared buffer.

    Returns:
        A :class:`ProducerConsumerResult` with counts and timing.
    """
    buf = BoundedBuffer(capacity=buffer_capacity)
    produced_counter = ThreadSafeCounter()
    consumed_counter = ThreadSafeCounter()
    items_per_producer = num_items // num_producers
    sentinel = object()
    start = time.perf_counter()

    def producer(pid: int) -> None:
        for i in range(items_per_producer):
            item = f"item-{pid}-{i}"
            buf.put(item)
            produced_counter.increment()
            logger.debug("Producer %d put %s", pid, item)
            time.sleep(0.01)  # simulate work

    def consumer(cid: int) -> None:
        while True:
            item = buf.get()
            if item is sentinel:
                buf.task_done()
                break
            consumed_counter.increment()
            logger.debug("Consumer %d got %s", cid, item)
            time.sleep(0.02)  # simulate processing
            buf.task_done()

    producers = [threading.Thread(target=producer, args=(i,), daemon=True) for i in range(num_producers)]
    consumers = [threading.Thread(target=consumer, args=(i,), daemon=True) for i in range(num_consumers)]

    for t in producers + consumers:
        t.start()
    for t in producers:
        t.join()

    # Send sentinel values to shut down consumers
    for _ in range(num_consumers):
        buf.put(sentinel)
    for t in consumers:
        t.join()

    duration = time.perf_counter() - start
    return ProducerConsumerResult(
        produced=produced_counter.value,
        consumed=consumed_counter.value,
        duration_seconds=round(duration, 4),
    )


# ---------------------------------------------------------------------------
# ThreadPoolExecutor utilities
# ---------------------------------------------------------------------------

def thread_pool_map(
    func: Callable[..., Any],
    items: Iterable[tuple[Any, ...]],
    *,
    max_workers: int = 4,
) -> list[Any]:
    """Apply *func* to each item in *items* using a thread pool.

    Args:
        func: Function to execute in each worker thread.
        items: An iterable of argument tuples.
        max_workers: Maximum number of worker threads.

    Returns:
        A list of results, one per input item.
    """
    results: list[Any] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(func, *args): args for args in items}
        for future in as_completed(futures):
            results.append(future.result())
    return results


def simulate_io_tasks(
    urls: list[str],
    delay: float = 0.1,
    max_workers: int = 4,
) -> list[dict[str, Any]]:
    """Simulate concurrent I/O tasks (e.g. HTTP requests).

    Args:
        urls: List of simulated URL strings.
        delay: Simulated I/O latency per request in seconds.
        max_workers: Number of threads.

    Returns:
        A list of result dicts, one per URL.
    """

    def _fetch(url: str) -> dict[str, Any]:
        time.sleep(delay)
        return {
            "url": url,
            "status": 200,
            "thread": threading.current_thread().name,
        }

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(_fetch, urls))


# ---------------------------------------------------------------------------
# Read-write lock
# ---------------------------------------------------------------------------

class ReadWriteLock:
    """A lock that allows concurrent reads but exclusive writes."""

    def __init__(self) -> None:
        self._readers = 0
        self._readers_lock = threading.Lock()
        self._write_lock = threading.Lock()

    def acquire_read(self) -> None:
        """Acquire a read lock."""
        with self._readers_lock:
            self._readers += 1
            if self._readers == 1:
                self._write_lock.acquire()

    def release_read(self) -> None:
        """Release a read lock."""
        with self._readers_lock:
            self._readers -= 1
            if self._readers == 0:
                self._write_lock.release()

    def acquire_write(self) -> None:
        """Acquire an exclusive write lock."""
        self._write_lock.acquire()

    def release_write(self) -> None:
        """Release the write lock."""
        self._write_lock.release()
