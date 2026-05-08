"""NumPy array utilities for vectorization and numerical operations."""

from __future__ import annotations

import numpy as np


def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """Normalize a vector to unit length while preserving shape."""
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def batch_dot(matrix: np.ndarray, vector: np.ndarray) -> np.ndarray:
    """Compute a batch dot product between a matrix and a vector."""
    return matrix.dot(vector)
