"""Core Python data type handling with parsing, casting, and normalization utilities.

This module is written for Python 3.10+ and demonstrates robust type conversion
patterns useful in data engineering and production pipelines.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, TypeVar

T = TypeVar("T")
PYTHON_VERSION = "3.10+"


def parse_bool(value: str) -> bool:
    """Convert a normalized string into a boolean value.

    Supported forms:
    - true values: true, 1, yes, y, t
    - false values: false, 0, no, n, f

    Args:
        value: The string to parse.

    Returns:
        A boolean value.

    Raises:
        ValueError: When the string cannot be interpreted as a boolean.
    """
    normalized = value.strip().lower()
    truthy = {"true", "1", "yes", "y", "t"}
    falsy = {"false", "0", "no", "n", "f"}

    if normalized in truthy:
        return True
    if normalized in falsy:
        return False

    raise ValueError(f"Unable to parse boolean value from {value!r}")


def parse_int(value: str, base: int = 10) -> int:
    """Parse a string into an integer using the specified numeric base."""
    return int(value.strip(), base=base)


def parse_float(value: str) -> float:
    """Parse a string into a floating point number."""
    return float(value.strip())


def parse_date(value: str, fmt: str = "%Y-%m-%d") -> date:
    """Parse a date string into a date object using a format string."""
    return datetime.strptime(value.strip(), fmt).date()


def parse_iso_datetime(value: str) -> datetime:
    """Parse an ISO-8601 string into a datetime object."""
    return datetime.fromisoformat(value)


def parse_list(value: str, separator: str = ",") -> list[str]:
    """Convert a separator-delimited string into a trimmed list of strings."""
    return [item.strip() for item in value.split(separator) if item.strip()]


def safe_cast(value: Any, target_type: type[T], default: T | None = None) -> T | None:
    """Attempt to cast a value to a target type and return a default on failure."""
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return default


def normalize_string(value: Any) -> str:
    """Normalize an input value into a trimmed lowercase string for comparison."""
    text = stringify(value)
    return text.strip().lower()


def stringify(value: Any) -> str:
    """Create a safe string representation for logging and diagnostics."""
    if value is None:
        return "<null>"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)
