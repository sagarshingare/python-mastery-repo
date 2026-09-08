"""CLI runner for NumPy array operations demonstrations."""

from __future__ import annotations

import argparse
import logging
import numpy as np

from numpy_lib.arrays.array_operations import (
    batch_dot,
    create_grid,
    filter_by_mask,
    flatten_array,
    matrix_properties,
    normalize_vector,
    replace_outliers,
    reshape_array,
    slice_submatrix,
    split_array,
    stack_arrays,
)

logger = logging.getLogger(__name__)


def run_creation_demo() -> None:
    logger.info("Running NumPy: Array Creation and Reshaping")
    arr = np.arange(12)
    reshaped = reshape_array(arr, (3, 4))
    print(f"Original 1D array [0..11] reshaped to (3, 4):\n{reshaped}")
    
    grid = create_grid(2, 3)
    print(f"\n2D Coordinate Grid shape: {grid.shape}")
    print(f"Top-left (0,0): {grid[0, 0]}, Bottom-right (1,2): {grid[1, 2]}")

    flattened = flatten_array(reshaped, copy=False)
    print(f"\nRaveled back to 1D: {flattened}")


def run_slicing_demo() -> None:
    logger.info("Running NumPy: Slicing and Stacking")
    matrix = np.arange(16).reshape(4, 4)
    print(f"4x4 Matrix:\n{matrix}")

    sub = slice_submatrix(matrix, 1, 3, 1, 3)
    print(f"\nInterior 2x2 Submatrix:\n{sub}")

    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    v_stacked = stack_arrays(a, b, "vertical")
    h_stacked = stack_arrays(a, b, "horizontal")
    print(f"\nVertical Stack:\n{v_stacked}")
    print(f"Horizontal Stack:\n{h_stacked}")

    splits = split_array(v_stacked, 2, axis=0)
    print(f"Split vertically into {len(splits)} chunks of shape {splits[0].shape}")


def run_manipulation_demo() -> None:
    logger.info("Running NumPy: Boolean Masking and Linear Algebra")
    data = np.array([-10.0, 5.0, 12.0, 99.0, 3.0, -50.0])
    cleaned = replace_outliers(data, lower_bound=0.0, upper_bound=50.0, fill_value=0.0)
    print(f"Raw data: {data}")
    print(f"Outliers (<0 or >50) replaced with 0.0: {cleaned}")

    vec = np.array([3.0, 4.0])
    norm_vec = normalize_vector(vec)
    print(f"\nVector [3, 4] normalized to unit length: {norm_vec} (norm = {np.linalg.norm(norm_vec):.2f})")

    sq_matrix = np.array([[2.0, 1.0], [1.0, 3.0]])
    props = matrix_properties(sq_matrix)
    print(f"\nSquare Matrix:\n{sq_matrix}")
    print(f"Determinant: {props['determinant']:.2f}, Trace: {props['trace']:.2f}, Norm: {props['norm']:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="NumPy Array Operations Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["creation", "slicing", "manipulation", "all"],
        default="all",
        help="Demonstration to run (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "creation": run_creation_demo,
        "slicing": run_slicing_demo,
        "manipulation": run_manipulation_demo,
    }

    if args.demo == "all":
        for fn in dispatch.values():
            fn()
            print()
    else:
        dispatch[args.demo]()


if __name__ == "__main__":
    main()
