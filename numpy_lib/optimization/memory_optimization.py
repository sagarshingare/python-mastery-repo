"""NumPy Memory Optimization: Contiguity, in-place computations, views vs copies, and downcasting."""

from __future__ import annotations

from typing import Any, Dict, Tuple

import numpy as np


def inspect_memory_layout(arr: np.ndarray) -> Dict[str, Any]:
    """Inspect array memory layout, contiguity flags, strides, and buffer footprint."""
    return {
        "shape": arr.shape,
        "dtype": str(arr.dtype),
        "nbytes": arr.nbytes,
        "itemsize": arr.itemsize,
        "c_contiguous": bool(arr.flags["C_CONTIGUOUS"]),
        "f_contiguous": bool(arr.flags["F_CONTIGUOUS"]),
        "strides": arr.strides,
        "shares_memory_with_base": arr.base is not None,
    }


def compute_in_place(arr: np.ndarray, scalar: float) -> Tuple[int, int]:
    """Demonstrate in-place mutation using out= parameter avoiding temporary buffer allocation."""
    original_id = id(arr)
    # Mutates arr in-place
    np.multiply(arr, scalar, out=arr)
    after_id = id(arr)
    return original_id, after_id


def optimize_numeric_dtypes(arr: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Downcast array dtypes to minimal safe precision to reduce memory footprint."""
    initial_bytes = arr.nbytes
    original_dtype = arr.dtype

    if np.issubdtype(arr.dtype, np.floating):
        # Downcast float64 to float32
        optimized = arr.astype(np.float32)
    elif np.issubdtype(arr.dtype, np.integer):
        min_val, max_val = arr.min(), arr.max()
        if min_val >= -128 and max_val <= 127:
            optimized = arr.astype(np.int8)
        elif min_val >= -32768 and max_val <= 32767:
            optimized = arr.astype(np.int16)
        elif min_val >= -2147483648 and max_val <= 2147483647:
            optimized = arr.astype(np.int32)
        else:
            optimized = arr
    else:
        optimized = arr

    saved_bytes = initial_bytes - optimized.nbytes
    savings_pct = (saved_bytes / initial_bytes * 100.0) if initial_bytes > 0 else 0.0

    metrics = {
        "original_dtype": str(original_dtype),
        "optimized_dtype": str(optimized.dtype),
        "original_bytes": initial_bytes,
        "optimized_bytes": optimized.nbytes,
        "savings_percentage": round(savings_pct, 1),
    }
    return optimized, metrics


def verify_view_vs_copy(original: np.ndarray) -> Dict[str, bool]:
    """Distinguish between views (shared memory buffer) and deep copies."""
    view = original[::2]
    copy = original.copy()

    return {
        "view_shares_memory": np.shares_memory(original, view),
        "view_has_base": view.base is original or (view.base is not None and np.shares_memory(view.base, original)),
        "copy_shares_memory": np.shares_memory(original, copy),
        "copy_has_base": copy.base is not None,
    }
