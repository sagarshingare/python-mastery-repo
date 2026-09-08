"""
Generator utilities demonstrating lazy evaluation, streaming data, and coroutines.
==================================================================================
Covers:
- Basic generator functions with `yield`
- Subgenerator delegation with `yield from` (PEP 380)
- Two-way generator communication (`.send()`, `.throw()`, `.close()`)
- Multi-stage memory-efficient streaming pipelines
- Chunking and batching lazy streams
"""

from __future__ import annotations
from collections.abc import Callable, Generator, Iterable
from typing import Any, Dict, List, Optional, TypeVar

T = TypeVar("T")
R = TypeVar("R")


# --- 1. Basic Generators & Streams ---

def fibonacci_generator(limit: int) -> Generator[int, None, None]:
    """Yield Fibonacci numbers up to the given limit."""
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b


def chunked_generator(sequence: Iterable[T], chunk_size: int) -> Generator[list[T], None, None]:
    """Yield chunks of the input sequence in fixed-size batches."""
    chunk: list[T] = []
    for item in sequence:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def filter_generator(sequence: Iterable[T], predicate: Callable[[T], bool]) -> Generator[T, None, None]:
    """Yield only values that satisfy the provided predicate."""
    for item in sequence:
        if predicate(item):
            yield item


def normalized_strings(strings: Iterable[str]) -> Generator[str, None, None]:
    """Yield normalized strings for streaming text processing."""
    for value in strings:
        yield value.strip().lower()


# --- 2. Subgenerator Delegation with yield from (PEP 380) ---

def flatten_nested(nested_sequence: Iterable[Any]) -> Generator[Any, None, None]:
    """Recursively flatten arbitrary nested iterables using `yield from`."""
    for item in nested_sequence:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten_nested(item)
        else:
            yield item


# --- 3. Coroutine-style Generators: send, throw, close ---

def running_average() -> Generator[float, float, None]:
    """Coroutine generator that accepts numeric inputs via `.send()` and yields running average."""
    total: float = 0.0
    count: int = 0
    average: float = 0.0

    while True:
        # Pauses and receives value sent via coroutine.send(val)
        new_val = yield average
        if new_val is None:
            continue
        total += new_val
        count += 1
        average = total / count


# --- 4. Multi-stage Streaming Pipeline ---

def stream_raw_events(count: int = 5) -> Generator[Dict[str, Any], None, None]:
    """Stage 1: Generate simulated high-volume event stream."""
    for i in range(1, count + 1):
        yield {"id": i, "amount": i * 25.5, "status": "COMPLETED" if i % 2 == 1 else "FAILED"}


def filter_completed_events(events: Iterable[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
    """Stage 2: Filter out non-completed records."""
    for ev in events:
        if ev.get("status") == "COMPLETED":
            yield ev


def apply_tax_and_format(events: Iterable[Dict[str, Any]], tax_rate: float = 0.08) -> Generator[Dict[str, Any], None, None]:
    """Stage 3: Enrich and compute total with tax in-flight."""
    for ev in events:
        base = ev["amount"]
        ev["total_with_tax"] = round(base * (1 + tax_rate), 2)
        yield ev


def run_pipeline(count: int = 6) -> List[Dict[str, Any]]:
    """Compose the multi-stage streaming pipeline without allocating intermediate lists."""
    pipeline = apply_tax_and_format(filter_completed_events(stream_raw_events(count)))
    return list(pipeline)
