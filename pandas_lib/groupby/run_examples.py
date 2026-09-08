"""Demonstrations for Pandas GroupBy operations."""

from __future__ import annotations

import argparse
import sys
import pandas as pd

from .groupby_operations import (
    aggregate_sales_by_department,
    calculate_group_zscore,
    calculate_percentage_of_group_total,
    filter_high_volume_groups,
    create_pivot_sales_summary,
)


def get_sample_sales_df() -> pd.DataFrame:
    """Provide realistic departmental sales data."""
    return pd.DataFrame(
        {
            "order_id": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            "department": [
                "Electronics",
                "Electronics",
                "Electronics",
                "Clothing",
                "Clothing",
                "Clothing",
                "Grocery",
                "Grocery",
                "Books",
                "Electronics",
            ],
            "region": [
                "North",
                "South",
                "North",
                "North",
                "East",
                "South",
                "North",
                "East",
                "West",
                "East",
            ],
            "revenue": [1200.0, 450.0, 850.0, 150.0, 220.0, 180.0, 95.0, 110.0, 45.0, 1400.0],
        }
    )


def demo_named_aggregation() -> None:
    df = get_sample_sales_df()
    print("--- 1. Departmental Named Aggregation ---")
    summary = aggregate_sales_by_department(df)
    print(summary.to_string(index=False))


def demo_transformations() -> None:
    df = get_sample_sales_df()
    print("\n--- 2. Group Transformations (Z-Scores & Percentage of Total) ---")
    df["z_score"] = calculate_group_zscore(df, "department", "revenue")
    df["pct_of_dept"] = calculate_percentage_of_group_total(df, "department", "revenue")
    print(df[["order_id", "department", "revenue", "z_score", "pct_of_dept"]].round(2).to_string(index=False))


def demo_filtering() -> None:
    df = get_sample_sales_df()
    print("\n--- 3. Group Filtering (min_count >= 3, min_revenue >= $500) ---")
    filtered = filter_high_volume_groups(df, "department", min_count=3, min_total_revenue=500.0)
    print(f"Retained {len(filtered)} rows belonging to high-volume departments:")
    print(filtered[["order_id", "department", "revenue"]].to_string(index=False))


def demo_pivot() -> None:
    df = get_sample_sales_df()
    print("\n--- 4. Pivot Sales Summary (Department vs Region) ---")
    pivot = create_pivot_sales_summary(df, index_cols="department", columns="region", values="revenue")
    print(pivot.to_string())


def main() -> None:
    parser = argparse.ArgumentParser(description="Pandas GroupBy Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["all", "agg", "transform", "filter", "pivot"],
        default="all",
        help="Specific GroupBy demonstration to run",
    )
    args = parser.parse_args()

    print("=== PANDAS GROUPBY DEMONSTRATIONS ===")
    if args.demo in ("all", "agg"):
        demo_named_aggregation()
    if args.demo in ("all", "transform"):
        demo_transformations()
    if args.demo in ("all", "filter"):
        demo_filtering()
    if args.demo in ("all", "pivot"):
        demo_pivot()


if __name__ == "__main__":
    main()
