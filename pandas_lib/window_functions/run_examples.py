"""Demonstrations for Pandas Window Functions."""

from __future__ import annotations

import argparse
import sys
import pandas as pd

from .window_operations import (
    calculate_rolling_metrics,
    calculate_expanding_metrics,
    calculate_exponential_moving_average,
    calculate_partitioned_ranks,
    calculate_lag_and_returns,
)


def get_sample_price_series() -> pd.DataFrame:
    dates = pd.date_range("2026-01-01", periods=6, freq="D")
    return pd.DataFrame(
        {
            "date": dates,
            "close": [100.0, 102.0, 101.0, 105.0, 107.0, 106.0],
        }
    )


def get_sample_sales_reps() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "region": ["East", "East", "East", "West", "West", "West"],
            "rep": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"],
            "sales": [50000, 75000, 50000, 82000, 95000, 61000],
        }
    )


def demo_rolling() -> None:
    df = get_sample_price_series()
    print("--- 1. Rolling Window Metrics (window=3) ---")
    res = calculate_rolling_metrics(df, "close", window=3)
    print(res.round(2).to_string(index=False))


def demo_expanding() -> None:
    df = get_sample_price_series()
    print("\n--- 2. Cumulative / Expanding Metrics ---")
    res = calculate_expanding_metrics(df, "close")
    print(res.round(2).to_string(index=False))


def demo_ema() -> None:
    df = get_sample_price_series()
    print("\n--- 3. Exponential Moving Average (span=3) ---")
    res = calculate_exponential_moving_average(df, "close", span=3)
    print(res.round(2).to_string(index=False))


def demo_ranking() -> None:
    df = get_sample_sales_reps()
    print("\n--- 4. Partitioned Ranking (Dense Rank by Region) ---")
    res = calculate_partitioned_ranks(df, group_col="region", value_col="sales", method="dense")
    print(res.sort_values(["region", "rank"]).to_string(index=False))


def demo_lag_lead() -> None:
    df = get_sample_price_series()
    print("\n--- 5. Shift, Lag, and Percentage Returns ---")
    res = calculate_lag_and_returns(df, value_col="close", periods=1)
    print(res.round(4).to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Pandas Window Functions Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["all", "rolling", "expanding", "ema", "ranking", "returns"],
        default="all",
        help="Specific window demonstration to run",
    )
    args = parser.parse_args()

    print("=== PANDAS WINDOW FUNCTIONS DEMONSTRATIONS ===")
    if args.demo in ("all", "rolling"):
        demo_rolling()
    if args.demo in ("all", "expanding"):
        demo_expanding()
    if args.demo in ("all", "ema"):
        demo_ema()
    if args.demo in ("all", "ranking"):
        demo_ranking()
    if args.demo in ("all", "returns"):
        demo_lag_lead()


if __name__ == "__main__":
    main()
