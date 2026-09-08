"""NumPy Memory Optimization module: Contiguity, in-place operations, and type downcasting."""

from .memory_optimization import (
    compute_in_place,
    inspect_memory_layout,
    optimize_numeric_dtypes,
    verify_view_vs_copy,
)

__all__ = [
    "inspect_memory_layout",
    "compute_in_place",
    "optimize_numeric_dtypes",
    "verify_view_vs_copy",
]
