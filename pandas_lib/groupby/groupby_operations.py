"""Pandas GroupBy operations: aggregations, transformations, filtering, and pivot tables."""

from __future__ import annotations

import logging
from typing import List, Union

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def aggregate_sales_by_department(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate financial and volume metrics across departments using named aggregation."""
    logger.debug("Aggregating sales by department across %d rows", len(df))
    summary = (
        df.groupby("department")
        .agg(
            total_revenue=("revenue", "sum"),
            average_ticket=("revenue", "mean"),
            max_ticket=("revenue", "max"),
            order_count=("order_id", "count"),
        )
        .reset_index()
    )
    # Sort descending by total revenue
    summary = summary.sort_values(by="total_revenue", ascending=False).reset_index(drop=True)
    return summary


def calculate_group_zscore(
    df: pd.DataFrame, group_col: str, value_col: str
) -> pd.Series:
    """Compute normalized z-scores within each group using transform.
    
    Formula: (x - group_mean) / group_std
    If std is 0, yields 0.0.
    """
    grouped = df.groupby(group_col)[value_col]
    mean = grouped.transform("mean")
    std = grouped.transform("std").fillna(0.0)

    # Avoid division by zero
    std_safe = std.replace(0.0, 1.0)
    zscore = (df[value_col] - mean) / std_safe
    # Mask rows where std was originally 0.0
    zscore = zscore.where(std > 0.0, 0.0)
    return zscore


def calculate_percentage_of_group_total(
    df: pd.DataFrame, group_col: str, value_col: str
) -> pd.Series:
    """Calculate each row's percentage contribution to its parent group total."""
    group_sum = df.groupby(group_col)[value_col].transform("sum")
    return (df[value_col] / group_sum) * 100.0


def filter_high_volume_groups(
    df: pd.DataFrame,
    group_col: str,
    min_count: int = 3,
    min_total_revenue: float = 500.0,
) -> pd.DataFrame:
    """Filter out groups that do not meet minimum order count and revenue thresholds."""
    filtered = df.groupby(group_col).filter(
        lambda g: len(g) >= min_count and g["revenue"].sum() >= min_total_revenue
    )
    return filtered.reset_index(drop=True)


def create_pivot_sales_summary(
    df: pd.DataFrame,
    index_cols: Union[str, List[str]],
    columns: str,
    values: str,
) -> pd.DataFrame:
    """Build a pivoted cross-tabulation table with total margins."""
    pivot = pd.pivot_table(
        df,
        index=index_cols,
        columns=columns,
        values=values,
        aggfunc="sum",
        fill_value=0.0,
        margins=True,
        margins_name="Total",
    )
    return pivot
