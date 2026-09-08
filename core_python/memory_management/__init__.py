"""
Memory management module for memory profiling, reference counting, and optimization.
"""

from .memory_utils import (
    CyclicNode,
    ExpensivePayload,
    MemoryReport,
    RegularDictObject,
    SlottedObject,
    WeakCache,
    analyze_memory,
    compare_slots_vs_dict,
    create_circular_reference_and_collect,
    get_reference_count,
    get_size,
)

__all__ = [
    "CyclicNode",
    "ExpensivePayload",
    "MemoryReport",
    "RegularDictObject",
    "SlottedObject",
    "WeakCache",
    "analyze_memory",
    "compare_slots_vs_dict",
    "create_circular_reference_and_collect",
    "get_reference_count",
    "get_size",
]