"""PySpark transformation examples - narrow vs wide transformations, aggregations, joins, and window analytics.

This module demonstrates PySpark transformations:
- Narrow transformations: filter, withColumn, select, map expressions (no shuffle)
- Wide transformations: groupBy aggregations, standard joins (trigger shuffle)
- Broadcast Joins: optimizing small-to-large table joins without cluster-wide shuffles
- Window Analytics: partitionBy, orderBy, ranking (row_number, dense_rank), and cumulative sums

Python version: 3.9+
"""

from __future__ import annotations

from typing import Any, List, Optional

try:
    from pyspark.sql import DataFrame, SparkSession, Window
    from pyspark.sql.functions import (
        avg,
        broadcast,
        col,
        count,
        dense_rank,
        lit,
        max as spark_max,
        min as spark_min,
        row_number,
        sum as spark_sum,
        when,
    )
    HAS_PYSPARK = True
except ImportError:  # pragma: no cover
    HAS_PYSPARK = False
    DataFrame = Any  # type: ignore[misc, assignment]


def apply_map_transformation(df: Optional[DataFrame], column: str, func: Any) -> Optional[DataFrame]:
    """Apply a transformation function or expression to a column.

    Args:
        df: DataFrame to transform.
        column: Column name to apply function to.
        func: Column expression or callable taking col(column).

    Returns:
        Transformed DataFrame with a new column `<column>_transformed`.
    """
    if df is None or not HAS_PYSPARK:
        return None

    if callable(func):
        return df.withColumn(f"{column}_transformed", func(col(column)))
    return df.withColumn(f"{column}_transformed", func)


def filter_greater_than(df: Optional[DataFrame], column: str, value: float) -> Optional[DataFrame]:
    """Filter rows where column value is greater than a specified threshold.

    Args:
        df: DataFrame to filter.
        column: Column name to filter on.
        value: Threshold value.

    Returns:
        Filtered DataFrame.
    """
    if df is None or not HAS_PYSPARK:
        return None

    return df.filter(col(column) > value)


def derive_columns(df: Optional[DataFrame]) -> Optional[DataFrame]:
    """Perform multiple narrow column additions and conditional categorization.

    Adds:
    - bonus: 10% of salary
    - total_comp: salary + bonus
    - tier: 'Senior' if salary >= 80000 else 'Standard'

    Args:
        df: Source DataFrame with 'salary' column.

    Returns:
        DataFrame with derived columns.
    """
    if df is None or not HAS_PYSPARK:
        return None

    return (
        df.withColumn("bonus", col("salary") * 0.10)
        .withColumn("total_comp", col("salary") + col("bonus"))
        .withColumn(
            "tier",
            when(col("salary") >= 80000.0, lit("Senior")).otherwise(lit("Standard")),
        )
    )


def group_and_aggregate(
    df: Optional[DataFrame],
    group_by_col: str,
    agg_col: str,
    agg_func: str = "sum",
) -> Optional[DataFrame]:
    """Group DataFrame by key and compute aggregate metrics (wide transformation).

    Args:
        df: DataFrame to aggregate.
        group_by_col: Column to group by.
        agg_col: Column to aggregate.
        agg_func: Aggregation metric ('sum', 'avg', 'count', 'min', 'max').

    Returns:
        Aggregated DataFrame with aliased output column.
    """
    if df is None or not HAS_PYSPARK:
        return None

    agg_map = {
        "sum": spark_sum(col(agg_col)),
        "avg": avg(col(agg_col)),
        "count": count(col(agg_col)),
        "min": spark_min(col(agg_col)),
        "max": spark_max(col(agg_col)),
    }

    expr = agg_map.get(agg_func.lower(), spark_sum(col(agg_col)))
    return df.groupBy(group_by_col).agg(expr.alias(f"{agg_func.lower()}_{agg_col}"))


def join_dataframes(
    left_df: Optional[DataFrame],
    right_df: Optional[DataFrame],
    join_key: str,
    how: str = "inner",
) -> Optional[DataFrame]:
    """Join two DataFrames on a specified key.

    Args:
        left_df: Left DataFrame.
        right_df: Right DataFrame.
        join_key: Column name shared by both DataFrames.
        how: Join type ('inner', 'left', 'right', 'outer').

    Returns:
        Joined DataFrame.
    """
    if left_df is None or right_df is None or not HAS_PYSPARK:
        return None

    return left_df.join(right_df, on=join_key, how=how)


def broadcast_join(
    large_df: Optional[DataFrame],
    small_df: Optional[DataFrame],
    join_key: str,
    how: str = "inner",
) -> Optional[DataFrame]:
    """Perform an optimized Broadcast Hash Join to eliminate shuffle stages.

    Broadcasts the small lookup table to all executor nodes.

    Args:
        large_df: Primary large dataset.
        small_df: Dimension or lookup dataset to broadcast.
        join_key: Common join key.
        how: Join type.

    Returns:
        Joined DataFrame via BroadcastHashJoin.
    """
    if large_df is None or small_df is None or not HAS_PYSPARK:
        return None

    return large_df.join(broadcast(small_df), on=join_key, how=how)


def apply_window_function(
    df: Optional[DataFrame],
    partition_col: str,
    order_col: str,
) -> Optional[DataFrame]:
    """Apply window ranking (row_number) partitioned by group and ordered descending.

    Args:
        df: DataFrame to rank.
        partition_col: Column to partition by (e.g., department).
        order_col: Column to order by (e.g., salary).

    Returns:
        DataFrame with added integer 'rank' column.
    """
    if df is None or not HAS_PYSPARK:
        return None

    window_spec = Window.partitionBy(partition_col).orderBy(col(order_col).desc())
    return df.withColumn("rank", row_number().over(window_spec))


def apply_window_analytics(
    df: Optional[DataFrame],
    partition_col: str,
    order_col: str,
    value_col: str,
) -> Optional[DataFrame]:
    """Apply advanced window metrics: dense_rank and running cumulative total.

    Args:
        df: DataFrame to process.
        partition_col: Group column.
        order_col: Sort column within partition.
        value_col: Numeric column to compute cumulative running total for.

    Returns:
        DataFrame with 'dense_rank' and 'running_total' columns.
    """
    if df is None or not HAS_PYSPARK:
        return None

    rank_spec = Window.partitionBy(partition_col).orderBy(col(order_col).desc())
    running_spec = (
        Window.partitionBy(partition_col)
        .orderBy(col(order_col).desc())
        .rowsBetween(Window.unboundedPreceding, Window.currentRow)
    )

    return df.withColumn("dense_rank", dense_rank().over(rank_spec)).withColumn(
        "running_total",
        spark_sum(col(value_col)).over(running_spec),
    )


def union_dataframes(df1: Optional[DataFrame], df2: Optional[DataFrame]) -> Optional[DataFrame]:
    """Union two DataFrames with identical schemas.

    Args:
        df1: First DataFrame.
        df2: Second DataFrame.

    Returns:
        Combined DataFrame.
    """
    if df1 is None or df2 is None or not HAS_PYSPARK:
        return None

    return df1.union(df2)