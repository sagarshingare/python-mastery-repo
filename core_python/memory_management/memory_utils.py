"""Memory management examples and reference patterns in Python."""

from __future__ import annotations

import gc
import sys
from dataclasses import dataclass
from typing import Any


def get_size(obj: Any, deep: bool = False) -> int:
    """Return the memory footprint of an object in bytes."""
    size = sys.getsizeof(obj)
    if deep and hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum(get_size(item, deep=True) for item in obj)
    return size


@dataclass
class MemoryReport:
    """A simple data class for memory usage reporting."""

    object_type: str
    shallow_size: int
    deep_size: int


def analyze_memory(obj: Any) -> MemoryReport:
    """Analyze memory usage for an object and return a structured report."""
    return MemoryReport(
        object_type=type(obj).__name__,
        shallow_size=get_size(obj, deep=False),
        deep_size=get_size(obj, deep=True),
    )


def collect_garbage() -> int:
    """Force garbage collection and return the number of unreachable objects collected."""
    return gc.collect()
