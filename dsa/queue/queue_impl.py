"""Queue implementations: standard, circular, and priority queue."""

from __future__ import annotations

import heapq
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Queue(Generic[T]):
    """A FIFO queue backed by a Python list.

    Example::

        q: Queue[str] = Queue()
        q.enqueue("a")
        q.enqueue("b")
        assert q.dequeue() == "a"
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    def enqueue(self, item: T) -> None:
        """Add an item to the back of the queue. O(1) amortised."""
        self._items.append(item)

    def dequeue(self) -> T:
        """Remove and return the front item. O(n).

        Raises:
            IndexError: If the queue is empty.
        """
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def peek(self) -> T:
        """Return the front item without removing it."""
        if not self._items:
            raise IndexError("peek on empty queue")
        return self._items[0]

    @property
    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Queue({self._items!r})"


class CircularQueue(Generic[T]):
    """A fixed-capacity circular (ring) buffer queue.

    Uses an array with head/tail pointers for O(1) enqueue and dequeue.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._buffer: list[T | None] = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    def enqueue(self, item: T) -> None:
        """Add an item. Raises OverflowError if full."""
        if self._size == self._capacity:
            raise OverflowError("Circular queue is full")
        self._buffer[self._tail] = item
        self._tail = (self._tail + 1) % self._capacity
        self._size += 1

    def dequeue(self) -> T:
        """Remove and return the front item."""
        if self._size == 0:
            raise IndexError("dequeue from empty circular queue")
        item = self._buffer[self._head]
        self._buffer[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return item  # type: ignore[return-value]

    def peek(self) -> T:
        """Return the front item without removing it."""
        if self._size == 0:
            raise IndexError("peek on empty circular queue")
        return self._buffer[self._head]  # type: ignore[return-value]

    @property
    def is_full(self) -> bool:
        return self._size == self._capacity

    @property
    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        items = []
        idx = self._head
        for _ in range(self._size):
            items.append(self._buffer[idx])
            idx = (idx + 1) % self._capacity
        return f"CircularQueue({items!r})"


class PriorityQueue:
    """A min-priority queue backed by ``heapq``.

    Items with lower priority values are dequeued first.
    """

    def __init__(self) -> None:
        self._heap: list[tuple[float, int, Any]] = []
        self._counter = 0  # tie-breaker for equal priorities

    def push(self, item: Any, priority: float = 0.0) -> None:
        """Add an item with the given priority."""
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def pop(self) -> Any:
        """Remove and return the highest-priority (lowest value) item."""
        if not self._heap:
            raise IndexError("pop from empty priority queue")
        _, _, item = heapq.heappop(self._heap)
        return item

    enqueue = push
    dequeue = pop

    def peek(self) -> Any:
        """Return the highest-priority item without removing it."""
        if not self._heap:
            raise IndexError("peek on empty priority queue")
        return self._heap[0][2]

    @property
    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def __len__(self) -> int:
        return len(self._heap)

    def __repr__(self) -> str:
        items = [(p, i) for p, _, i in sorted(self._heap)]
        return f"PriorityQueue({items!r})"


class Deque(Generic[T]):
    """A double-ended queue supporting O(1) operations at both ends."""

    def __init__(self) -> None:
        from collections import deque
        self._items: deque[T] = deque()

    def push_front(self, item: T) -> None:
        """Add an item to the front."""
        self._items.appendleft(item)

    def push_back(self, item: T) -> None:
        """Add an item to the back."""
        self._items.append(item)

    def pop_front(self) -> T:
        """Remove and return the front item."""
        if not self._items:
            raise IndexError("pop from empty deque")
        return self._items.popleft()

    def pop_back(self) -> T:
        """Remove and return the back item."""
        if not self._items:
            raise IndexError("pop from empty deque")
        return self._items.pop()

    append_left = push_front
    append_right = push_back
    pop_left = pop_front
    pop_right = pop_back

    def peek_front(self) -> T:
        """Return the front item without removing it."""
        if not self._items:
            raise IndexError("peek on empty deque")
        return self._items[0]

    def peek_back(self) -> T:
        """Return the back item without removing it."""
        if not self._items:
            raise IndexError("peek on empty deque")
        return self._items[-1]

    peek_left = peek_front
    peek_right = peek_back

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Deque({list(self._items)!r})"
