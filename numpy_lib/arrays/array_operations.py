"""NumPy array utilities: Creation, slicing, reshaping, stacking, and linear algebra."""

from __future__ import annotations

from typing import Tuple

import numpy as np


def create_grid(rows: int, cols: int, step: float = 1.0) -> np.ndarray:
    """Create a 2D meshgrid coordinate array."""
    x = np.arange(0, cols * step, step)
    y = np.arange(0, rows * step, step)
    xx, yy = np.meshgrid(x, y)
    return np.dstack([xx, yy])


def reshape_array(arr: np.ndarray, target_shape: Tuple[int, ...]) -> np.ndarray:
    """Safely reshape an array or compute dimension inferred with -1."""
    return arr.reshape(target_shape)


def flatten_array(arr: np.ndarray, copy: bool = False) -> np.ndarray:
    """Flatten array to 1D: ravel (view when possible) vs flatten (copy)."""
    return arr.flatten() if copy else arr.ravel()


def slice_submatrix(
    matrix: np.ndarray,
    row_start: int,
    row_end: int,
    col_start: int,
    col_end: int,
    step: int = 1,
) -> np.ndarray:
    """Extract a 2D strided submatrix slice."""
    return matrix[row_start:row_end:step, col_start:col_end:step]


def stack_arrays(
    a: np.ndarray,
    b: np.ndarray,
    direction: str = "vertical",
) -> np.ndarray:
    """Stack two arrays horizontally ('horizontal') or vertically ('vertical')."""
    if direction == "horizontal":
        return np.hstack((a, b))
    elif direction == "vertical":
        return np.vstack((a, b))
    elif direction == "depth":
        return np.dstack((a, b))
    else:
        raise ValueError(f"Unknown direction '{direction}'. Choose horizontal, vertical, or depth.")


def split_array(arr: np.ndarray, num_sections: int, axis: int = 0) -> list[np.ndarray]:
    """Split an array into equal or sub-equal sections along an axis."""
    return np.array_split(arr, num_sections, axis=axis)


def filter_by_mask(arr: np.ndarray, condition: np.ndarray) -> np.ndarray:
    """Extract elements that satisfy a boolean mask condition."""
    return arr[condition]


def replace_outliers(arr: np.ndarray, lower_bound: float, upper_bound: float, fill_value: float) -> np.ndarray:
    """Replace elements outside [lower_bound, upper_bound] with a specified fill value."""
    result = arr.copy()
    result[(result < lower_bound) | (result > upper_bound)] = fill_value
    return result


def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """Normalize a vector to unit length while preserving shape."""
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def batch_dot(matrix: np.ndarray, vector: np.ndarray) -> np.ndarray:
    """Compute a batch dot product between a matrix and a vector."""
    return matrix.dot(vector)


def matrix_properties(matrix: np.ndarray) -> dict[str, float]:
    """Compute matrix determinant, trace, and Frobenius norm."""
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Matrix must be 2D square for determinant and trace.")
    return {
        "determinant": float(np.linalg.det(matrix)),
        "trace": float(np.trace(matrix)),
        "norm": float(np.linalg.norm(matrix)),
    }
