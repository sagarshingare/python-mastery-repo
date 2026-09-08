"""CLI runner for NumPy broadcasting demonstrations."""

from __future__ import annotations

import argparse
import logging
import numpy as np

from numpy_lib.broadcasting.broadcasting_examples import (
    center_and_scale,
    check_broadcast_compatibility,
    expand_dimension,
    outer_product_grid,
    pairwise_euclidean_distance,
)

logger = logging.getLogger(__name__)


def run_rules_demo() -> None:
    logger.info("Running Broadcasting: Compatibility Rules")
    pairs = [
        ((3, 4), (4,)),
        ((2, 1, 5), (3, 5)),
        ((4, 3), (3, 4)),
        ((1, 5), (5, 1)),
    ]
    for s_a, s_b in pairs:
        compatible, res = check_broadcast_compatibility(s_a, s_b)
        status = f"✅ Broadcasts to {res}" if compatible else "❌ Incompatible"
        print(f"Shape A: {str(s_a).ljust(10)} + Shape B: {str(s_b).ljust(10)} -> {status}")


def run_expansion_demo() -> None:
    logger.info("Running Broadcasting: Dimension Expansion & Scaling")
    X = np.array([[10.0, 200.0], [20.0, 400.0], [30.0, 600.0]])
    print(f"Raw feature matrix (3 samples, 2 features):\n{X}")

    std_X, mean, std = center_and_scale(X)
    print(f"\nColumn Means: {mean}, Column Stds: {std}")
    print(f"Standardized X (zero mean, unit variance):\n{std_X}")

    a = np.array([1, 2, 3])
    b = np.array([10, 20, 30, 40])
    outer = outer_product_grid(a, b)
    print(f"\nOuter Product Grid (3x1 * 1x4 = 3x4):\n{outer}")


def run_distance_demo() -> None:
    logger.info("Running Broadcasting: Vectorized Pairwise Euclidean Distance")
    # 3 points in 2D space
    X = np.array([[0.0, 0.0], [3.0, 4.0], [1.0, 1.0]])
    # 2 target query points in 2D space
    Y = np.array([[0.0, 0.0], [3.0, 0.0]])

    distances = pairwise_euclidean_distance(X, Y)
    print("Coordinates X (3 points):\n", X)
    print("Coordinates Y (2 query centers):\n", Y)
    print(f"\nPairwise Euclidean Distance Matrix (shape {distances.shape}):\n{distances}")


def main() -> None:
    parser = argparse.ArgumentParser(description="NumPy Broadcasting Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["rules", "expansion", "distance", "all"],
        default="all",
        help="Demonstration to run (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "rules": run_rules_demo,
        "expansion": run_expansion_demo,
        "distance": run_distance_demo,
    }

    if args.demo == "all":
        for fn in dispatch.values():
            fn()
            print()
    else:
        dispatch[args.demo]()


if __name__ == "__main__":
    main()
