"""Vectorization patterns: Universal functions (ufuncs), np.where/select branching, and cumulative metrics."""

from __future__ import annotations

import time
from typing import Dict, List, Tuple

import numpy as np


def relu(x: np.ndarray) -> np.ndarray:
    """Vectorized Rectified Linear Unit activation."""
    return np.maximum(0.0, x)


def sigmoid(x: np.ndarray) -> np.ndarray:
    """Numerically stable vectorized Sigmoid activation."""
    clipped = np.clip(x, -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(-clipped))


def categorize_values(scores: np.ndarray) -> np.ndarray:
    """Vectorized multi-branch condition evaluation using np.select."""
    conditions = [
        scores >= 90,
        scores >= 80,
        scores >= 70,
        scores >= 60,
    ]
    choices = ["A", "B", "C", "D"]
    return np.select(conditions, choices, default="F")


def cumulative_drawdown(prices: np.ndarray) -> np.ndarray:
    """Compute percentage drawdown series from historical peak using maximum.accumulate."""
    peaks = np.maximum.accumulate(prices)
    # Avoid zero division
    safe_peaks = np.where(peaks == 0, 1.0, peaks)
    drawdowns = (prices - safe_peaks) / safe_peaks
    return drawdowns


def compute_moving_window_diff(arr: np.ndarray, lag: int = 1) -> np.ndarray:
    """Compute vectorized differences between values separated by lag."""
    return arr[lag:] - arr[:-lag]


def benchmark_loop_vs_vectorized(n: int = 200000) -> Dict[str, float]:
    """Benchmark vectorized arithmetic vs native Python for-loop."""
    py_list = list(range(n))
    np_arr = np.arange(n, dtype=np.float64)

    # 1. Native Python loop
    t0 = time.perf_counter()
    _ = [x ** 2 + 2 * x + 1 for x in py_list]
    t_loop = time.perf_counter() - t0

    # 2. NumPy vectorized
    t1 = time.perf_counter()
    _ = np_arr ** 2 + 2 * np_arr + 1
    t_vec = time.perf_counter() - t1

    speedup = t_loop / t_vec if t_vec > 0 else float("inf")
    return {
        "n_elements": float(n),
        "loop_seconds": t_loop,
        "vectorized_seconds": t_vec,
        "speedup_factor": round(speedup, 1),
    }
