"""
Python Descriptors Protocol
===========================
Descriptors are the fundamental protocol powering:
- `property`
- `classmethod` & `staticmethod`
- `__slots__`
- ORM fields (SQLAlchemy, Django models)
- Validation frameworks (Pydantic, marshmallow)

Descriptor Protocol:
- Non-data descriptor: implements `__get__` only. Precedence is lower than instance __dict__.
- Data descriptor: implements `__set__` and/or `__delete__` (alongside `__get__`). Precedence is higher than instance __dict__.
- `__set_name__(self, owner, name)`: introduced in Python 3.6, automatically called when the owner class is constructed.
"""

from __future__ import annotations
import re
from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar

T = TypeVar("T")
V = TypeVar("V")


class ReadOnlyDescriptor:
    """Non-data descriptor providing lazy-evaluated / memoized read-only attribute."""

    def __init__(self, func: Callable[[Any], Any]) -> None:
        self.func = func
        self.name: Optional[str] = None

    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.name = name

    def __get__(self, instance: Optional[Any], owner: Optional[Type[Any]] = None) -> Any:
        if instance is None:
            return self
        assert self.name is not None
        # Cache the result directly on the instance __dict__
        # Because this is a NON-DATA descriptor, next lookup will find it in instance.__dict__ directly!
        val = self.func(instance)
        instance.__dict__[self.name] = val
        return val


class ValidatedField(Generic[T]):
    """Data descriptor that validates and stores attribute values in instance dict."""

    def __init__(self, default: Optional[T] = None) -> None:
        self.default = default
        self.name: str = ""
        self.storage_name: str = ""

    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.name = name
        self.storage_name = f"_descriptor_{name}"

    def __get__(self, instance: Optional[Any], owner: Optional[Type[Any]] = None) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, self.default)

    def __set__(self, instance: Any, value: T) -> None:
        self.validate(value)
        setattr(instance, self.storage_name, value)

    def __delete__(self, instance: Any) -> None:
        if hasattr(instance, self.storage_name):
            delattr(instance, self.storage_name)

    def validate(self, value: T) -> None:
        """Override in subclasses to enforce validation logic."""
        pass


class Typed(ValidatedField[T]):
    """Enforces strict runtime type validation."""

    def __init__(self, expected_type: Type[T], default: Optional[T] = None) -> None:
        super().__init__(default=default)
        self.expected_type = expected_type

    def validate(self, value: Any) -> None:
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Field '{self.name}' must be of type {self.expected_type.__name__}, "
                f"got {type(value).__name__} ({value!r})"
            )


class PositiveNumber(ValidatedField[float]):
    """Enforces that numeric field must be strictly positive (> 0)."""

    def validate(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(f"Field '{self.name}' must be numeric, got {type(value).__name__}")
        if value <= 0:
            raise ValueError(f"Field '{self.name}' must be positive (> 0), got {value}")


class BoundedString(ValidatedField[str]):
    """Enforces non-empty string within min and max length bounds."""

    def __init__(self, min_len: int = 1, max_len: int = 255) -> None:
        super().__init__()
        self.min_len = min_len
        self.max_len = max_len

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"Field '{self.name}' must be a string, got {type(value).__name__}")
        if not (self.min_len <= len(value) <= self.max_len):
            raise ValueError(
                f"Field '{self.name}' length must be between {self.min_len} and {self.max_len} chars, "
                f"got length {len(value)}"
            )


class EmailField(ValidatedField[str]):
    """Validates email format using regex pattern."""

    EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

    def validate(self, value: str) -> None:
        if not isinstance(value, str) or not self.EMAIL_REGEX.match(value):
            raise ValueError(f"Field '{self.name}' must be a valid email address, got {value!r}")


class UserAccount:
    """Production example demonstrating declarative model validation using Descriptors."""

    username = BoundedString(min_len=3, max_len=30)
    email = EmailField()
    balance = PositiveNumber()

    def __init__(self, username: str, email: str, balance: float) -> None:
        self.username = username
        self.email = email
        self.balance = balance

    @ReadOnlyDescriptor
    def expensive_hash(self) -> str:
        """Computed once on first access, then fetched from instance dict (non-data descriptor magic)."""
        import hashlib
        return hashlib.sha256(f"{self.username}:{self.email}".encode()).hexdigest()

    def __repr__(self) -> str:
        return f"UserAccount(username={self.username!r}, email={self.email!r}, balance={self.balance})"


def run_descriptor_demos() -> None:
    """Run all descriptor protocol demonstrations."""
    print("=== Python Descriptors Protocol Demo ===")

    user = UserAccount("alice_dev", "alice@example.com", 250.0)
    print(f"Created user: {user}")
    print(f"Computed expensive hash (lazy): {user.expensive_hash}")
    # Second access pulls directly from user.__dict__['expensive_hash']
    print(f"Cached in __dict__: {'expensive_hash' in user.__dict__}")

    # Validation tests
    try:
        user.balance = -10.0
    except ValueError as err:
        print(f"Caught expected validation error: {err}")

    try:
        user.email = "not-an-email"
    except ValueError as err:
        print(f"Caught expected email validation error: {err}")

    try:
        user.username = "al"  # Too short (< 3)
    except ValueError as err:
        print(f"Caught expected length validation error: {err}")

    print("Descriptors demo completed successfully!\n")


if __name__ == "__main__":
    run_descriptor_demos()
