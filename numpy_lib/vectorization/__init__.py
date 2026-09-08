"""NumPy Vectorization module: Ufuncs, conditional branching, and SIMD optimizations."""

from .vectorization_patterns import (
    benchmark_loop_vs_vectorized,
    categorize_values,
    compute_moving_window_diff,
    cumulative_drawdown,
    relu,
    sigmoid,
)

__all__ = [
    "relu",
    "sigmoid",
    "categorize_values",
    "cumulative_drawdown",
    "compute_moving_window_diff",
    "benchmark_loop_vs_vectorized",
]
