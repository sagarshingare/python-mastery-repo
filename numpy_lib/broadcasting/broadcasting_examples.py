"""NumPy Broadcasting rules, dimension expansion, feature standardization, and pairwise metrics."""

from __future__ import annotations

from typing import Tuple

import numpy as np


def check_broadcast_compatibility(shape_a: Tuple[int, ...], shape_b: Tuple[int, ...]) -> Tuple[bool, Tuple[int, ...]]:
    """Determine if two shapes can broadcast together according to NumPy trailing-dimension rules."""
    len_a, len_b = len(shape_a), len(shape_b)
    max_len = max(len_a, len_b)

    # Pad shorter shape with 1s on the left
    padded_a = (1,) * (max_len - len_a) + shape_a
    padded_b = (1,) * (max_len - len_b) + shape_b

    result_shape = []
    for dim_a, dim_b in zip(padded_a, padded_b):
        if dim_a == dim_b:
            result_shape.append(dim_a)
        elif dim_a == 1:
            result_shape.append(dim_b)
        elif dim_b == 1:
            result_shape.append(dim_a)
        else:
            return False, ()

    return True, tuple(result_shape)


def expand_dimension(arr: np.ndarray, axis: int) -> np.ndarray:
    """Insert a new singleton axis at the specified index."""
    return np.expand_dims(arr, axis=axis)


def center_and_scale(X: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Standardize feature matrix X (Z-score normalization) using column-wise broadcasting."""
    mean = np.mean(X, axis=0)  # Shape (D,)
    std = np.std(X, axis=0)    # Shape (D,)
    # Avoid zero division
    safe_std = np.where(std == 0, 1.0, std)
    standardized = (X - mean) / safe_std  # (N, D) - (D,) / (D,)
    return standardized, mean, std


def outer_product_grid(vec_a: np.ndarray, vec_b: np.ndarray) -> np.ndarray:
    """Compute outer product of two 1D vectors using dimension expansion broadcasting."""
    # (M, 1) * (1, N) -> (M, N)
    return vec_a[:, np.newaxis] * vec_b[np.newaxis, :]


def pairwise_euclidean_distance(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Compute pairwise Euclidean distance matrix between X (N, D) and Y (M, D) without loops."""
    # X[:, np.newaxis, :] shape: (N, 1, D)
    # Y[np.newaxis, :, :] shape: (1, M, D)
    diff = X[:, np.newaxis, :] - Y[np.newaxis, :, :]  # shape: (N, M, D)
    return np.sqrt(np.sum(diff ** 2, axis=-1))          # shape: (N, M)
