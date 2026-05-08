"""Generator utilities demonstrating lazy evaluation and streaming data."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Generator


def fibonacci_generator(limit: int) -> Generator[int, None, None]:
    """Yield Fibonacci numbers up to the given limit."""
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b


def chunked_generator(sequence: Iterable[int], chunk_size: int) -> Generator[list[int], None, None]:
    """Yield chunks of the input sequence in fixed-size batches."""
    chunk: list[int] = []
    for item in sequence:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def filter_generator(sequence: Iterable[int], predicate: Callable[[int], bool]) -> Generator[int, None, None]:
    """Yield only values that satisfy the provided predicate."""
    for item in sequence:
        if predicate(item):
            yield item


def normalized_strings(strings: Iterable[str]) -> Generator[str, None, None]:
    """Yield normalized strings for streaming text processing."""
    for value in strings:
        yield value.strip().lower()
