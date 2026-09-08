"""Stack implementations and classic stack-based algorithms."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """A LIFO stack backed by a Python list.

    Example::

        s: Stack[int] = Stack()
        s.push(10)
        s.push(20)
        assert s.pop() == 20
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """Push an item onto the stack. O(1) amortised."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top item. O(1).

        Raises:
            IndexError: If the stack is empty.
        """
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        """Return the top item without removing it."""
        if not self._items:
            raise IndexError("peek on empty stack")
        return self._items[-1]

    @property
    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"


class MinStack(Generic[T]):
    """A stack that supports O(1) retrieval of the minimum element.

    Maintains a parallel stack of running minimums.
    """

    def __init__(self) -> None:
        self._items: list[T] = []
        self._mins: list[T] = []

    def push(self, item: T) -> None:
        """Push an item and update the minimum tracker."""
        self._items.append(item)
        if not self._mins or item <= self._mins[-1]:  # type: ignore[operator]
            self._mins.append(item)

    def pop(self) -> T:
        """Remove and return the top item."""
        if not self._items:
            raise IndexError("pop from empty MinStack")
        item = self._items.pop()
        if item == self._mins[-1]:
            self._mins.pop()
        return item

    def get_min(self) -> T:
        """Return the current minimum in O(1)."""
        if not self._mins:
            raise IndexError("MinStack is empty")
        return self._mins[-1]

    def __len__(self) -> int:
        return len(self._items)


# ---------------------------------------------------------------------------
# Classic stack algorithms
# ---------------------------------------------------------------------------

_BRACKET_MAP = {")": "(", "]": "[", "}": "{"}


def is_balanced(expression: str) -> bool:
    """Check whether brackets in *expression* are balanced.

    Supports ``()``, ``[]``, and ``{}``.

    Args:
        expression: String containing brackets.

    Returns:
        True if all brackets are properly matched and nested.
    """
    stack: list[str] = []
    for char in expression:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack or stack[-1] != _BRACKET_MAP[char]:
                return False
            stack.pop()
    return len(stack) == 0


def evaluate_postfix(expression: str) -> float:
    """Evaluate a postfix (Reverse Polish Notation) expression.

    Tokens must be separated by spaces.

    Args:
        expression: e.g. ``"3 4 + 2 *"`` → 14.

    Returns:
        The evaluated result.

    Raises:
        ValueError: If the expression is malformed.
    """
    stack: list[float] = []
    operators = {"+", "-", "*", "/"}

    for token in expression.split():
        if token in operators:
            if len(stack) < 2:
                raise ValueError(f"Not enough operands for '{token}'")
            b, a = stack.pop(), stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                if b == 0:
                    raise ValueError("Division by zero")
                stack.append(a / b)
        else:
            stack.append(float(token))

    if len(stack) != 1:
        raise ValueError("Malformed expression")
    return stack[0]


def next_greater_element(nums: list[int]) -> list[int]:
    """Find the next greater element for each position in *nums*.

    Returns a list where ``result[i]`` is the next element greater than
    ``nums[i]`` to its right, or ``-1`` if none exists. O(n).
    """
    result = [-1] * len(nums)
    stack: list[int] = []  # stack of indices

    for i in range(len(nums)):
        while stack and nums[stack[-1]] < nums[i]:
            result[stack.pop()] = nums[i]
        stack.append(i)

    return result
