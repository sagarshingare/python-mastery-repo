"""Linked list implementations: singly linked and doubly linked."""

from __future__ import annotations

from typing import Any, Generator


class SinglyNode:
    """Node for a singly linked list."""

    __slots__ = ("value", "next")

    def __init__(self, value: Any, next_node: SinglyNode | None = None) -> None:
        self.value = value
        self.next = next_node

    def __repr__(self) -> str:
        return f"SinglyNode({self.value!r})"


class SinglyLinkedList:
    """A singly linked list with standard operations.

    Supports insertion, deletion, reversal, cycle detection, and iteration.

    Example::

        ll = SinglyLinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        assert list(ll) == [1, 2, 3]
    """

    def __init__(self) -> None:
        self.head: SinglyNode | None = None
        self._size: int = 0

    # --- Insertion ---

    def prepend(self, value: Any) -> None:
        """Insert a value at the head of the list. O(1)."""
        self.head = SinglyNode(value, self.head)
        self._size += 1

    def append(self, value: Any) -> None:
        """Insert a value at the tail of the list. O(n)."""
        new_node = SinglyNode(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def insert_at(self, index: int, value: Any) -> None:
        """Insert a value at a given index. O(n).

        Raises:
            IndexError: If *index* is out of range.
        """
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range for list of size {self._size}")
        if index == 0:
            self.prepend(value)
            return
        current = self.head
        for _ in range(index - 1):
            current = current.next  # type: ignore[union-attr]
        current.next = SinglyNode(value, current.next)  # type: ignore[union-attr]
        self._size += 1

    # --- Deletion ---

    def delete_value(self, value: Any) -> bool:
        """Delete the first occurrence of *value*. Returns True if found."""
        if self.head is None:
            return False
        if self.head.value == value:
            self.head = self.head.next
            self._size -= 1
            return True
        current = self.head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def delete_at(self, index: int) -> Any:
        """Delete and return the value at *index*. O(n).

        Raises:
            IndexError: If the list is empty or *index* is out of range.
        """
        if self.head is None or index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range")
        if index == 0:
            value = self.head.value
            self.head = self.head.next
            self._size -= 1
            return value
        current = self.head
        for _ in range(index - 1):
            current = current.next  # type: ignore[union-attr]
        target = current.next  # type: ignore[union-attr]
        current.next = target.next  # type: ignore[union-attr]
        self._size -= 1
        return target.value  # type: ignore[union-attr]

    # --- Search & access ---

    def search(self, value: Any) -> int:
        """Return the index of the first occurrence of *value*, or -1."""
        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def get(self, index: int) -> Any:
        """Return the value at *index*. O(n)."""
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range")
        current = self.head
        for _ in range(index):
            current = current.next  # type: ignore[union-attr]
        return current.value  # type: ignore[union-attr]

    # --- Reversal ---

    def reverse(self) -> None:
        """Reverse the list in-place. O(n) time, O(1) space."""
        prev: SinglyNode | None = None
        current = self.head
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    # --- Cycle detection ---

    def has_cycle(self) -> bool:
        """Detect a cycle using Floyd's tortoise-and-hare algorithm."""
        slow = self.head
        fast = self.head
        while fast is not None and fast.next is not None:
            slow = slow.next  # type: ignore[union-attr]
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    # --- Middle element ---

    def find_middle(self) -> Any | None:
        """Return the middle element (slow-fast pointer technique)."""
        if self.head is None:
            return None
        slow = self.head
        fast = self.head
        while fast.next is not None and fast.next.next is not None:
            slow = slow.next  # type: ignore[union-attr]
            fast = fast.next.next
        return slow.value  # type: ignore[union-attr]

    # --- Dunder methods ---

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Generator[Any, None, None]:
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __bool__(self) -> bool:
        return self._size > 0

    def __repr__(self) -> str:
        return f"SinglyLinkedList({list(self)!r})"

    def __str__(self) -> str:
        return " -> ".join(str(v) for v in self) or "Empty"

    def __contains__(self, value: Any) -> bool:
        return self.search(value) != -1

    def to_list(self) -> list[Any]:
        """Return elements as a Python list."""
        return list(self)

    def find(self, value: Any) -> SinglyNode | None:
        """Find and return node containing value, or None."""
        current = self.head
        while current is not None:
            if current.value == value:
                return current
            current = current.next
        return None

    delete = delete_value
    middle_node = find_middle


# ---------------------------------------------------------------------------
# Doubly Linked List
# ---------------------------------------------------------------------------

class DoublyNode:
    """Node for a doubly linked list."""

    __slots__ = ("value", "prev", "next")

    def __init__(
        self,
        value: Any,
        prev_node: DoublyNode | None = None,
        next_node: DoublyNode | None = None,
    ) -> None:
        self.value = value
        self.prev = prev_node
        self.next = next_node


class DoublyLinkedList:
    """A doubly linked list with O(1) append and prepend."""

    def __init__(self) -> None:
        self.head: DoublyNode | None = None
        self.tail: DoublyNode | None = None
        self._size: int = 0

    def prepend(self, value: Any) -> None:
        """Insert a value at the head. O(1)."""
        new_node = DoublyNode(value, next_node=self.head)
        if self.head is not None:
            self.head.prev = new_node
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self._size += 1

    def append(self, value: Any) -> None:
        """Insert a value at the tail. O(1)."""
        new_node = DoublyNode(value, prev_node=self.tail)
        if self.tail is not None:
            self.tail.next = new_node
        self.tail = new_node
        if self.head is None:
            self.head = new_node
        self._size += 1

    def delete_value(self, value: Any) -> bool:
        """Delete the first occurrence of *value*. Returns True if found."""
        current = self.head
        while current is not None:
            if current.value == value:
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self._size -= 1
                return True
            current = current.next
        return False

    def reverse(self) -> None:
        """Reverse the list in-place. O(n)."""
        current = self.head
        while current is not None:
            current.prev, current.next = current.next, current.prev
            current = current.prev  # moving forward (prev is now next)
        self.head, self.tail = self.tail, self.head

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Generator[Any, None, None]:
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        return f"DoublyLinkedList([{', '.join(repr(v) for v in self)}])"

    def to_list(self) -> list[Any]:
        """Return elements as a Python list."""
        return list(self)

    def to_list_reversed(self) -> list[Any]:
        """Return elements in reverse order as a Python list."""
        items: list[Any] = []
        current = self.tail
        while current is not None:
            items.append(current.value)
            current = current.prev
        return items

    delete = delete_value
