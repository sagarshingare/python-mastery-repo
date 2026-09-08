"""Heap implementations and heap-based algorithms."""

from __future__ import annotations

import heapq
from typing import Any


class MinHeap:
    """A min-heap backed by a Python list.

    The smallest element is always at the root.
    """

    def __init__(self, items: list[Any] | None = None) -> None:
        self._data: list[Any] = list(items) if items else []
        heapq.heapify(self._data)

    def push(self, value: Any) -> None:
        """Insert a value into the heap. O(log n)."""
        heapq.heappush(self._data, value)

    def pop(self) -> Any:
        """Remove and return the smallest element. O(log n)."""
        if not self._data:
            raise IndexError("pop from empty heap")
        return heapq.heappop(self._data)

    def peek(self) -> Any:
        """Return the smallest element without removing it. O(1)."""
        if not self._data:
            raise IndexError("peek on empty heap")
        return self._data[0]

    def pushpop(self, value: Any) -> Any:
        """Push *value* then pop the smallest. More efficient than separate calls."""
        return heapq.heappushpop(self._data, value)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"MinHeap({self._data!r})"


class MaxHeap:
    """A max-heap implemented by negating values in a min-heap."""

    def __init__(self, items: list[Any] | None = None) -> None:
        self._data: list[Any] = [-x for x in items] if items else []
        heapq.heapify(self._data)

    def push(self, value: Any) -> None:
        """Insert a value. O(log n)."""
        heapq.heappush(self._data, -value)

    def pop(self) -> Any:
        """Remove and return the largest element. O(log n)."""
        if not self._data:
            raise IndexError("pop from empty heap")
        return -heapq.heappop(self._data)

    def peek(self) -> Any:
        """Return the largest element. O(1)."""
        if not self._data:
            raise IndexError("peek on empty heap")
        return -self._data[0]

    def __len__(self) -> int:
        return len(self._data)


# ---------------------------------------------------------------------------
# Heap algorithms
# ---------------------------------------------------------------------------

def heapsort(data: list[Any]) -> list[Any]:
    """Sort *data* using heapsort. O(n log n), not in-place."""
    heap = MinHeap(data)
    return [heap.pop() for _ in range(len(heap))]


def top_k_elements(data: list[Any], k: int) -> list[Any]:
    """Return the *k* largest elements from *data*. O(n log k)."""
    if k <= 0:
        return []
    return heapq.nlargest(k, data)


def k_smallest_elements(data: list[Any], k: int) -> list[Any]:
    """Return the *k* smallest elements from *data*. O(n log k)."""
    if k <= 0:
        return []
    return heapq.nsmallest(k, data)


def merge_k_sorted_lists(lists: list[list[Any]]) -> list[Any]:
    """Merge *k* sorted lists into a single sorted list. O(n log k)."""
    return list(heapq.merge(*lists))


def find_median_stream(stream: list[int]) -> list[float]:
    """Compute the running median of a stream of integers.

    Uses two heaps: a max-heap for the lower half and a min-heap
    for the upper half. O(n log n) total.
    """
    low: list[int] = []   # max-heap (negated)
    high: list[int] = []  # min-heap
    medians: list[float] = []

    for num in stream:
        heapq.heappush(low, -num)
        heapq.heappush(high, -heapq.heappop(low))

        if len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))

        if len(low) > len(high):
            medians.append(float(-low[0]))
        else:
            medians.append((-low[0] + high[0]) / 2.0)

    return medians
