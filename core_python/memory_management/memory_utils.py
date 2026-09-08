"""
Memory management, reference counting, cyclic garbage collection, and __slots__ in Python.
==========================================================================================
Covers:
- Reference counting mechanics via `sys.getrefcount()`
- Circular reference cycles and cyclic GC (`gc.collect()`, `gc.get_count()`)
- Weak references (`weakref.ref`, `weakref.WeakValueDictionary`)
- Memory profiling with `tracemalloc`
- Memory footprint optimization: `__slots__` vs standard instance `__dict__`
"""

from __future__ import annotations
from dataclasses import dataclass
import gc
import sys
import time
import tracemalloc
from typing import Any, Dict, List, Optional
import weakref


# --- 1. Memory Sizing & Reporting ---

def get_size(obj: Any, deep: bool = False) -> int:
    """Return the memory footprint of an object in bytes."""
    size = sys.getsizeof(obj)
    if deep and hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum(get_size(item, deep=True) for item in obj)
    return size


@dataclass
class MemoryReport:
    """Data class for memory usage reporting."""
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


# --- 2. Reference Counting & sys.getrefcount ---

def get_reference_count(obj: Any) -> int:
    """Return the current reference count of obj (subtracting 1 for the argument ref)."""
    # Note: passing obj into sys.getrefcount creates a temporary reference
    return sys.getrefcount(obj) - 1


# --- 3. Circular References & Cyclic Garbage Collection ---

class CyclicNode:
    """Class designed to demonstrate circular reference formation."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.partner: Optional[CyclicNode] = None

    def __repr__(self) -> str:
        return f"CyclicNode({self.name})"


def create_circular_reference_and_collect() -> int:
    """Creates an isolated reference cycle, drops local references, and triggers gc.collect()."""
    node_a = CyclicNode("NodeA")
    node_b = CyclicNode("NodeB")
    node_a.partner = node_b
    node_b.partner = node_a

    # Delete local names: the objects still reference each other, creating an isolated cycle
    del node_a
    del node_b

    # Force cyclic garbage collector to identify and free the unreachable cycle
    unreachable_collected = gc.collect()
    return unreachable_collected


# --- 4. Weak References (weakref) ---

class ExpensivePayload:
    """Object stored in a weak reference cache."""

    def __init__(self, key: str, payload_size: int = 1000) -> None:
        self.key = key
        self.data = [0] * payload_size


class WeakCache:
    """Cache that does not prevent cached values from being garbage collected."""

    def __init__(self) -> None:
        self._cache: weakref.WeakValueDictionary[str, ExpensivePayload] = weakref.WeakValueDictionary()

    def set(self, key: str, value: ExpensivePayload) -> None:
        self._cache[key] = value

    def get(self, key: str) -> Optional[ExpensivePayload]:
        return self._cache.get(key)

    def size(self) -> int:
        return len(self._cache)


# --- 5. Memory Optimization: __slots__ vs __dict__ ---

class RegularDictObject:
    """Standard class allocating a per-instance __dict__."""

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z


class SlottedObject:
    """Memory-optimized class reserving fixed descriptors without __dict__."""

    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z


def compare_slots_vs_dict(count: int = 20000) -> Dict[str, Any]:
    """Measures memory allocated for count instances of regular vs slotted objects."""
    gc.collect()

    # Measure RegularDictObject
    tracemalloc.start()
    regular_items = [RegularDictObject(float(i), float(i + 1), float(i + 2)) for i in range(count)]
    current_reg, peak_reg = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del regular_items
    gc.collect()

    # Measure SlottedObject
    tracemalloc.start()
    slotted_items = [SlottedObject(float(i), float(i + 1), float(i + 2)) for i in range(count)]
    current_slot, peak_slot = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del slotted_items
    gc.collect()

    savings_pct = round(((peak_reg - peak_slot) / peak_reg) * 100, 2) if peak_reg > 0 else 0.0

    return {
        "count": count,
        "regular_peak_bytes": peak_reg,
        "slotted_peak_bytes": peak_slot,
        "memory_saved_percent": savings_pct,
    }
