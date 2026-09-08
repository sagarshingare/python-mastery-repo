"""CLI runner for NumPy memory optimization demonstrations."""

from __future__ import annotations

import argparse
import logging
import numpy as np

from numpy_lib.optimization.memory_optimization import (
    compute_in_place,
    inspect_memory_layout,
    optimize_numeric_dtypes,
    verify_view_vs_copy,
)

logger = logging.getLogger(__name__)


def run_layout_demo() -> None:
    logger.info("Running Memory Optimization: Contiguity & Strides")
    c_arr = np.ones((3, 4), dtype=np.float64, order="C")
    f_arr = np.ones((3, 4), dtype=np.float64, order="F")
    
    print("C-Contiguous Matrix (Row-Major):")
    print(inspect_memory_layout(c_arr))
    print("\nFortran-Contiguous Matrix (Column-Major):")
    print(inspect_memory_layout(f_arr))


def run_in_place_demo() -> None:
    logger.info("Running Memory Optimization: In-Place Computations")
    arr = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float64)
    orig_id, after_id = compute_in_place(arr, 10.0)
    print(f"Array values multiplied by 10 in-place: {arr}")
    print(f"Original ID: {orig_id}, After ID: {after_id} (Same memory pointer: {orig_id == after_id})")

    check = verify_view_vs_copy(arr)
    print("\nView vs Copy Verification:")
    print(f"  View shares memory: {check['view_shares_memory']}")
    print(f"  Copy shares memory: {check['copy_shares_memory']}")


def run_downcast_demo() -> None:
    logger.info("Running Memory Optimization: Numeric Type Downcasting")
    large_floats = np.random.randn(10000)  # default float64
    _, float_metrics = optimize_numeric_dtypes(large_floats)
    print("Float Downcasting (float64 -> float32):")
    print(f"  Original: {float_metrics['original_bytes']} bytes ({float_metrics['original_dtype']})")
    print(f"  Optimized: {float_metrics['optimized_bytes']} bytes ({float_metrics['optimized_dtype']})")
    print(f"  Savings: {float_metrics['savings_percentage']}%")

    ints = np.random.randint(0, 100, size=10000, dtype=np.int64)
    _, int_metrics = optimize_numeric_dtypes(ints)
    print("\nInteger Downcasting (int64 -> int8):")
    print(f"  Original: {int_metrics['original_bytes']} bytes ({int_metrics['original_dtype']})")
    print(f"  Optimized: {int_metrics['optimized_bytes']} bytes ({int_metrics['optimized_dtype']})")
    print(f"  Savings: {int_metrics['savings_percentage']}%")


def main() -> None:
    parser = argparse.ArgumentParser(description="NumPy Memory Optimization Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["layout", "in_place", "downcast", "all"],
        default="all",
        help="Demonstration to run (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "layout": run_layout_demo,
        "in_place": run_in_place_demo,
        "downcast": run_downcast_demo,
    }

    if args.demo == "all":
        for fn in dispatch.values():
            fn()
            print()
    else:
        dispatch[args.demo]()


if __name__ == "__main__":
    main()
