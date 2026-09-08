"""CLI runner for NumPy vectorization demonstrations."""

from __future__ import annotations

import argparse
import logging
import numpy as np

from numpy_lib.vectorization.vectorization_patterns import (
    benchmark_loop_vs_vectorized,
    categorize_values,
    compute_moving_window_diff,
    cumulative_drawdown,
    relu,
    sigmoid,
)

logger = logging.getLogger(__name__)


def run_conditionals_demo() -> None:
    logger.info("Running Vectorization: Activations & Multi-Branching")
    inputs = np.array([-5.0, -1.0, 0.0, 2.0, 10.0])
    print(f"Inputs:  {inputs}")
    print(f"ReLU:    {relu(inputs)}")
    print(f"Sigmoid: {sigmoid(inputs).round(4)}")

    scores = np.array([95, 82, 74, 61, 55, 88])
    grades = categorize_values(scores)
    print(f"\nStudent scores: {scores}")
    print(f"Letter grades (via np.select): {grades}")


def run_reductions_demo() -> None:
    logger.info("Running Vectorization: Financial Drawdowns & Cumulative Reductions")
    prices = np.array([100.0, 105.0, 102.0, 98.0, 110.0, 108.0, 95.0])
    drawdowns = cumulative_drawdown(prices)
    print(f"Asset Prices: {prices}")
    print("Drawdown from peak:")
    for p, dd in zip(prices, drawdowns):
        print(f"  Price ${p:,.2f} -> Drawdown: {dd * 100:+.2f}%")

    diffs = compute_moving_window_diff(prices, lag=1)
    print(f"\n1-Period Price Differences: {diffs.round(2)}")


def run_benchmark_demo() -> None:
    logger.info("Running Vectorization: Loop vs SIMD Benchmark")
    results = benchmark_loop_vs_vectorized(n=200000)
    print(f"Elements: {int(results['n_elements']):,}")
    print(f"  Python loop time:      {results['loop_seconds']:.4f}s")
    print(f"  NumPy vectorized time: {results['vectorized_seconds']:.4f}s")
    print(f"  Speedup Factor:        {results['speedup_factor']}x faster")


def main() -> None:
    parser = argparse.ArgumentParser(description="NumPy Vectorization Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["conditionals", "reductions", "benchmark", "all"],
        default="all",
        help="Demonstration to run (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "conditionals": run_conditionals_demo,
        "reductions": run_reductions_demo,
        "benchmark": run_benchmark_demo,
    }

    if args.demo == "all":
        for fn in dispatch.values():
            fn()
            print()
    else:
        dispatch[args.demo]()


if __name__ == "__main__":
    main()
