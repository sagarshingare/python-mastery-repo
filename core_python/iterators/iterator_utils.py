"""
Iterator utilities demonstrating custom iteration, sequence traversal, and itertools patterns.
=============================================================================================
Covers:
- Iterator Protocol (`__iter__`, `__next__`, `StopIteration`)
- Iterable vs Iterator distinction (multi-pass collections vs single-pass streams)
- Two-argument sentinel iterators (`iter(callable, sentinel)`)
- Reversible protocol (`__reversed__`)
- Lookahead with `PeekableIterator`
- Key itertools power patterns (`pairwise`, `take`, `group_consecutive`)
"""

from __future__ import annotations
from collections.abc import Iterable, Iterator
import itertools
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar

T = TypeVar("T")


# --- 1. Basic Iterator Protocol ---

class RangeIterator(Iterator[int]):
    """A simple iterator for a numeric range."""

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> RangeIterator:
        return self

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += self.step
        return value


# --- 2. Iterable vs Iterator (Multi-Pass Collection) ---

class DatasetCollection(Iterable[T]):
    """An Iterable collection that supports multiple independent iterations without exhaustion."""

    def __init__(self, items: List[T]) -> None:
        self._items = items

    def __iter__(self) -> Iterator[T]:
        # Returns a fresh iterator each time __iter__() is called!
        return iter(self._items)

    def __reversed__(self) -> Iterator[T]:
        """Implements the reversible protocol."""
        return reversed(self._items)

    def __len__(self) -> int:
        return len(self._items)


# --- 3. Sentinel Iterators ---

def read_until_sentinel(producer: Callable[[], T], sentinel: T) -> List[T]:
    """Demonstrates two-argument `iter(callable, sentinel)`.

    Calls producer() repeatedly until it produces the sentinel value.
    Extremely common for reading fixed-size chunks from network sockets or files.
    """
    return list(iter(producer, sentinel))


# --- 4. Iteration Helpers & itertools Patterns ---

def take(sequence: Iterable[T], count: int) -> list[T]:
    """Return the first count items from an iterable using itertools.islice."""
    return list(itertools.islice(sequence, count))


def pairwise(sequence: Iterable[T]) -> Iterator[tuple[T, T]]:
    """Yield successive overlapping pairs from the input sequence."""
    iterator = iter(sequence)
    try:
        previous = next(iterator)
    except StopIteration:
        return
    for current in iterator:
        yield previous, current
        previous = current


def group_consecutive(sequence: Iterable[T]) -> Dict[T, int]:
    """Count consecutive runs of elements using itertools.groupby."""
    counts: Dict[T, int] = {}
    for key, group in itertools.groupby(sequence):
        counts[key] = counts.get(key, 0) + len(list(group))
    return counts


class PeekableIterator(Iterator[T]):
    """A peekable iterator that can look ahead one value without consuming it."""

    def __init__(self, sequence: Iterable[T]) -> None:
        self._iterator = iter(sequence)
        self._cache: list[T] = []

    def __iter__(self) -> PeekableIterator[T]:
        return self

    def __next__(self) -> T:
        if self._cache:
            return self._cache.pop(0)
        return next(self._iterator)

    def peek(self) -> T:
        if not self._cache:
            self._cache.append(next(self._iterator))
        return self._cache[0]
