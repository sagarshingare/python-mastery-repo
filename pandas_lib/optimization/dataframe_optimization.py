"""Pandas performance and memory optimization: dtype downcasting, category types, and vectorization vs apply benchmarks."""

from __future__ import annotations

import logging
import time
from typing import Any, Callable, Dict, Generator, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def get_memory_usage_report(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate exact memory usage of a DataFrame across all columns."""
    mem_series = df.memory_usage(deep=True)
    total_bytes = mem_series.sum()
    col_breakdown = {
        col: int(mem_series[col]) for col in df.columns
    }
    return {
        "total_bytes": int(total_bytes),
        "total_kb": round(total_bytes / 1024, 2),
        "total_mb": round(total_bytes / (1024 * 1024), 4),
        "columns": col_breakdown,
    }


def optimize_dtypes(
    df: pd.DataFrame,
    categorical_threshold: float = 0.5,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Downcast numeric columns and convert low-cardinality object columns to category.
    
    Returns the optimized DataFrame and a summary of memory reduction.
    """
    initial_bytes = df.memory_usage(deep=True).sum()
    optimized = df.copy()

    for col in optimized.columns:
        col_type = optimized[col].dtype

        # Downcast integers and floats
        if pd.api.types.is_integer_dtype(col_type):
            if (optimized[col] >= 0).all():
                optimized[col] = pd.to_numeric(optimized[col], downcast="unsigned")
            else:
                optimized[col] = pd.to_numeric(optimized[col], downcast="integer")
        elif pd.api.types.is_float_dtype(col_type):
            optimized[col] = pd.to_numeric(optimized[col], downcast="float")
        elif pd.api.types.is_object_dtype(col_type) or pd.api.types.is_string_dtype(col_type):
            num_unique = optimized[col].nunique()
            num_total = len(optimized[col])
            if num_total > 0 and (num_unique / num_total) < categorical_threshold:
                optimized[col] = optimized[col].astype("category")

    final_bytes = optimized.memory_usage(deep=True).sum()
    reduction_pct = 0.0
    if initial_bytes > 0:
        reduction_pct = ((initial_bytes - final_bytes) / initial_bytes) * 100.0

    stats = {
        "initial_bytes": int(initial_bytes),
        "final_bytes": int(final_bytes),
        "saved_bytes": int(initial_bytes - final_bytes),
        "reduction_pct": round(reduction_pct, 2),
    }
    logger.info("Optimized DataFrame: %s", stats)
    return optimized, stats


def chunk_dataframe(
    df: pd.DataFrame,
    chunk_size: int = 1000,
) -> Generator[pd.DataFrame, None, None]:
    """Yield DataFrame slices in memory-bounded chunks."""
    for start in range(0, len(df), chunk_size):
        yield df.iloc[start : start + chunk_size]


def benchmark_vectorized_vs_apply(n_rows: int = 50_000) -> Dict[str, float]:
    """Benchmark vectorized arithmetic vs df.apply(lambda row: ...)."""
    np.random.seed(42)
    df = pd.DataFrame(
        {
            "price": np.random.uniform(10.0, 500.0, size=n_rows),
            "quantity": np.random.randint(1, 20, size=n_rows),
            "discount": np.random.uniform(0.0, 0.3, size=n_rows),
        }
    )

    # 1. df.apply (row-by-row iteration)
    t0 = time.perf_counter()
    _ = df.apply(lambda row: (row["price"] * row["quantity"]) * (1.0 - row["discount"]), axis=1)
    apply_time = time.perf_counter() - t0

    # 2. Vectorized operations
    t1 = time.perf_counter()
    _ = (df["price"] * df["quantity"]) * (1.0 - df["discount"])
    vectorized_time = time.perf_counter() - t1

    speedup = apply_time / max(vectorized_time, 1e-9)
    return {
        "rows": float(n_rows),
        "apply_time_sec": round(apply_time, 4),
        "vectorized_time_sec": round(vectorized_time, 4),
        "speedup_factor": round(speedup, 1),
    }
