"""Optimization subpackage for Pandas memory footprint, downcasting, and vectorization."""

from .dataframe_optimization import (
    optimize_dtypes,
    get_memory_usage_report,
    chunk_dataframe,
    benchmark_vectorized_vs_apply,
)

__all__ = [
    "optimize_dtypes",
    "get_memory_usage_report",
    "chunk_dataframe",
    "benchmark_vectorized_vs_apply",
]
