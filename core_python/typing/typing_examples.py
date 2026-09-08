"""Type annotation examples covering modern Python typing features."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    Literal,
    NamedTuple,
    NewType,
    Protocol,
    TypedDict,
    TypeVar,
    overload,
    runtime_checkable,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# TypeVar and Generics
# ---------------------------------------------------------------------------

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class Stack(Generic[T]):
    """A generic LIFO stack.

    Example::

        stack: Stack[int] = Stack()
        stack.push(1)
        stack.push(2)
        assert stack.pop() == 2
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """Push an item onto the stack."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top item.

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
        """Whether the stack has no items."""
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"


class Registry(Generic[K, V]):
    """A generic key-value registry with type-safe lookup.

    Demonstrates multi-parameter generics.
    """

    def __init__(self) -> None:
        self._store: dict[K, V] = {}

    def register(self, key: K, value: V) -> None:
        """Register a value under the given key."""
        self._store[key] = value

    def lookup(self, key: K) -> V | None:
        """Look up a value by key, returning ``None`` if missing."""
        return self._store.get(key)

    def __contains__(self, key: K) -> bool:
        return key in self._store


# ---------------------------------------------------------------------------
# Protocols (structural subtyping)
# ---------------------------------------------------------------------------

@runtime_checkable
class Serializable(Protocol):
    """Protocol for objects that can serialise themselves to a dict."""

    def to_dict(self) -> dict[str, Any]:
        """Convert the object to a dictionary."""
        ...


@runtime_checkable
class Comparable(Protocol):
    """Protocol for objects that support less-than comparison."""

    def __lt__(self, other: Any) -> bool:
        ...


def find_minimum(items: list[Comparable]) -> Comparable:
    """Return the smallest item using the ``Comparable`` protocol.

    Args:
        items: Non-empty list of comparable objects.

    Raises:
        ValueError: If *items* is empty.
    """
    if not items:
        raise ValueError("Cannot find minimum of an empty list")
    return min(items)


# ---------------------------------------------------------------------------
# TypedDict
# ---------------------------------------------------------------------------

class UserProfile(TypedDict):
    """A typed dictionary representing a user profile."""

    id: int
    username: str
    email: str
    is_active: bool


class ApiResponse(TypedDict, total=False):
    """A typed dictionary for API responses with optional fields."""

    status: int
    message: str
    data: list[dict[str, Any]]
    error: str


def create_user_profile(
    user_id: int,
    username: str,
    email: str,
    *,
    is_active: bool = True,
) -> UserProfile:
    """Factory for creating type-safe user profiles."""
    return UserProfile(
        id=user_id,
        username=username,
        email=email,
        is_active=is_active,
    )


# ---------------------------------------------------------------------------
# Literal types
# ---------------------------------------------------------------------------

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]


def configure_log_level(level: LogLevel) -> str:
    """Set the logging level and return a confirmation string.

    Only the five standard levels are accepted (enforced at type-check time).
    """
    numeric = getattr(logging, level)
    logging.getLogger().setLevel(numeric)
    return f"Log level set to {level}"


# ---------------------------------------------------------------------------
# NewType
# ---------------------------------------------------------------------------

UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)


def get_user_order(user_id: UserId, order_id: OrderId) -> dict[str, int]:
    """Demonstrate NewType for domain-specific IDs.

    ``UserId`` and ``OrderId`` are both ``int`` at runtime but distinct
    at type-check time, preventing accidental swaps.
    """
    return {"user_id": user_id, "order_id": order_id}


# ---------------------------------------------------------------------------
# Function overloads
# ---------------------------------------------------------------------------

@overload
def normalize(value: str) -> str: ...


@overload
def normalize(value: int) -> int: ...


@overload
def normalize(value: float) -> float: ...


def normalize(value: str | int | float) -> str | int | float:
    """Normalize a value depending on its type.

    - ``str`` → stripped and lowercased.
    - ``int`` → absolute value.
    - ``float`` → rounded to 2 decimal places.
    """
    if isinstance(value, str):
        return value.strip().lower()
    if isinstance(value, int):
        return abs(value)
    return round(value, 2)


# ---------------------------------------------------------------------------
# NamedTuple
# ---------------------------------------------------------------------------

class Coordinate(NamedTuple):
    """An immutable 2-D coordinate."""

    x: float
    y: float

    def distance_to(self, other: Coordinate) -> float:
        """Euclidean distance to *other*."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


# ---------------------------------------------------------------------------
# Dataclass with generic constraint
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Result(Generic[T]):
    """A result wrapper that holds either a value or an error message.

    Follows the Result/Either pattern common in typed functional code.
    """

    value: T | None = None
    error: str | None = None

    @property
    def is_ok(self) -> bool:
        """Whether this result represents success."""
        return self.error is None

    @classmethod
    def ok(cls, value: T) -> Result[T]:
        """Create a success result."""
        return cls(value=value)

    @classmethod
    def fail(cls, error: str) -> Result[Any]:
        """Create a failure result."""
        return cls(error=error)
