"""Demonstrations for Pandas Merge and Join operations."""

from __future__ import annotations

import argparse
import sys
import pandas as pd

from .merge_operations import (
    perform_relational_merge,
    join_on_index,
    concatenate_dataframes,
    merge_asof_timestamps,
    validate_cardinality_merge,
)


def get_sample_customers_orders() -> tuple[pd.DataFrame, pd.DataFrame]:
    customers = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4],
            "customer_name": ["Alice", "Bob", "Charlie", "Diana"],
            "tier": ["Gold", "Silver", "Gold", "Bronze"],
        }
    )
    orders = pd.DataFrame(
        {
            "order_id": [1001, 1002, 1003, 1004],
            "customer_id": [1, 2, 1, 5],
            "amount": [250.0, 80.0, 420.0, 15.0],
        }
    )
    return customers, orders


def demo_relational_merges() -> None:
    customers, orders = get_sample_customers_orders()
    print("--- 1. Relational Merges (Inner, Left, Outer with Indicator) ---")

    inner = perform_relational_merge(customers, orders, on="customer_id", how="inner")
    print("\n[INNER JOIN]:")
    print(inner.to_string(index=False))

    outer_diag = perform_relational_merge(customers, orders, on="customer_id", how="outer", indicator=True)
    print("\n[FULL OUTER JOIN with _merge indicator]:")
    print(outer_diag.to_string(index=False))


def demo_index_joins() -> None:
    print("\n--- 2. Index-Based Join ---")
    df1 = pd.DataFrame({"metric_a": [10, 20, 30]}, index=["row1", "row2", "row3"])
    df2 = pd.DataFrame({"metric_b": [100, 200]}, index=["row1", "row2"])
    joined = join_on_index(df1, df2, how="left")
    print(joined)


def demo_concatenation() -> None:
    print("\n--- 3. Vertical & Horizontal Concatenation ---")
    batch_q1 = pd.DataFrame({"id": [1, 2], "val": [10, 20]})
    batch_q2 = pd.DataFrame({"id": [3, 4], "val": [30, 40]})
    vertical = concatenate_dataframes([batch_q1, batch_q2], axis=0)
    print("[Vertical Concat]:\n", vertical.to_string(index=False))


def demo_asof_merge() -> None:
    print("\n--- 4. Time-Series Merge Asof (Matching Nearest Past Quote) ---")
    trades = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2026-01-01 09:30:05", "2026-01-01 09:30:15"]),
            "symbol": ["AAPL", "AAPL"],
            "shares": [100, 50],
        }
    )
    quotes = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2026-01-01 09:30:00", "2026-01-01 09:30:10", "2026-01-01 09:30:20"]
            ),
            "symbol": ["AAPL", "AAPL", "AAPL"],
            "bid": [150.10, 150.25, 150.40],
            "ask": [150.15, 150.30, 150.45],
        }
    )
    asof_matched = merge_asof_timestamps(trades, quotes, on="timestamp", by="symbol", direction="backward")
    print(asof_matched.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Pandas Join and Merge Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["all", "relational", "index", "concat", "asof"],
        default="all",
        help="Specific Join demonstration to run",
    )
    args = parser.parse_args()

    print("=== PANDAS JOIN & MERGE DEMONSTRATIONS ===")
    if args.demo in ("all", "relational"):
        demo_relational_merges()
    if args.demo in ("all", "index"):
        demo_index_joins()
    if args.demo in ("all", "concat"):
        demo_concatenation()
    if args.demo in ("all", "asof"):
        demo_asof_merge()


if __name__ == "__main__":
    main()
