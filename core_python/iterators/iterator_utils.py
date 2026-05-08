"""Iterator utilities demonstrating custom iteration and sequence traversal."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Iterable, TypeVar

T = TypeVar("T")


class RangeIterator(Iterator[int]):
    """A simple iterator for a numeric range."""

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        self.current = start
        self.stop = stop
        self.step = step

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += self.step
        return value


def take(sequence: Iterable[T], count: int) -> list[T]:
    """Return the first count items from an iterable."""
    result: list[T] = []
    for index, item in enumerate(sequence):
        if index >= count:
            break
        result.append(item)
    return result


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
