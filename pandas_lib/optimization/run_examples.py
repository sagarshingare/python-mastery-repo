"""Demonstrations for Pandas Performance and Memory Optimization."""

from __future__ import annotations

import argparse
import sys
import numpy as np
import pandas as pd

from .dataframe_optimization import (
    optimize_dtypes,
    get_memory_usage_report,
    chunk_dataframe,
    benchmark_vectorized_vs_apply,
)


def create_unoptimized_df(n_rows: int = 10_000) -> pd.DataFrame:
    np.random.seed(42)
    regions = ["North", "South", "East", "West"]
    categories = ["Tech", "Home", "Fashion", "Grocery", "Auto"]
    return pd.DataFrame(
        {
            "id": np.arange(n_rows, dtype="int64"),
            "region": np.random.choice(regions, size=n_rows),
            "category": np.random.choice(categories, size=n_rows),
            "quantity": np.random.randint(1, 50, size=n_rows, dtype="int64"),
            "price": np.random.uniform(5.0, 500.0, size=n_rows),  # float64
        }
    )


def demo_memory_downcasting() -> None:
    print("--- 1. Memory Optimization (Dtype Downcasting & Categoricals) ---")
    df = create_unoptimized_df(10_000)
    rep_before = get_memory_usage_report(df)
    print(f"Before optimization: {rep_before['total_kb']} KB")
    print("Column types before:\n", df.dtypes)

    optimized_df, stats = optimize_dtypes(df)
    rep_after = get_memory_usage_report(optimized_df)
    print(f"\nAfter optimization:  {rep_after['total_kb']} KB")
    print(f"Memory reduction:    {stats['reduction_pct']}% saved!")
    print("Column types after:\n", optimized_df.dtypes)


def demo_chunking() -> None:
    print("\n--- 2. Memory-Bounded Chunk Processing ---")
    df = create_unoptimized_df(5_000)
    chunk_size = 1_000
    print(f"Streaming {len(df)} rows in batches of {chunk_size} rows:")
    batch_totals = []
    for idx, chunk in enumerate(chunk_dataframe(df, chunk_size=chunk_size), 1):
        batch_sum = (chunk["quantity"] * chunk["price"]).sum()
        batch_totals.append(batch_sum)
        print(f"  Chunk {idx}: {len(chunk)} rows processed, revenue=${batch_sum:,.2f}")
    print(f"Total revenue processed across chunks: ${sum(batch_totals):,.2f}")


def demo_vectorization_benchmark() -> None:
    print("\n--- 3. Vectorization vs .apply() Performance Benchmark ---")
    print("Benchmarking 50,000 row batch arithmetic...")
    res = benchmark_vectorized_vs_apply(n_rows=50_000)
    print(f"  df.apply() (row-by-row) time: {res['apply_time_sec']:.4f}s")
    print(f"  Vectorized expression time:   {res['vectorized_time_sec']:.4f}s")
    print(f"  ⚡ Speedup:                   {res['speedup_factor']}x faster!")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pandas Optimization Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["all", "downcast", "chunk", "benchmark"],
        default="all",
        help="Specific optimization demonstration to run",
    )
    args = parser.parse_args()

    print("=== PANDAS PERFORMANCE & OPTIMIZATION DEMONSTRATIONS ===")
    if args.demo in ("all", "downcast"):
        demo_memory_downcasting()
    if args.demo in ("all", "chunk"):
        demo_chunking()
    if args.demo in ("all", "benchmark"):
        demo_vectorization_benchmark()


if __name__ == "__main__":
    main()
