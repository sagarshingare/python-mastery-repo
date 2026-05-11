"""PySpark transformation examples - map, filter, flatMap, groupBy, aggregations.

This module demonstrates PySpark transformation concepts including:
- Map and FlatMap transformations
- Filter operations
- GroupBy and aggregations
- Joins and unions
- Window functions

Python version: 3.9+
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

try:
    from pyspark.sql import SparkSession, Window
    from pyspark.sql.functions import col, sum as spark_sum, avg, count, row_number
    HAS_PYSPARK = True
except ImportError:
    HAS_PYSPARK = False


def apply_map_transformation(df: Any, column: str, func: Any) -> Any:
    """Apply a transformation function to a column using map.
    
    Args:
        df: DataFrame to transform.
        column: Column name to apply function to.
        func: Function to apply.
        
    Returns:
        Transformed DataFrame.
    """
    if df is None or not HAS_PYSPARK:
        return None
    
    return df.withColumn(f"{column}_transformed", func(col(column)))


def filter_greater_than(df: Any, column: str, value: float) -> Any:
    """Filter rows where column value is greater than threshold.
    
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


def group_and_aggregate(df: Any, group_by_col: str, agg_col: str, agg_func: str = "sum") -> Any:
    """Group DataFrame and apply aggregation.
    
    Args:
        df: DataFrame to aggregate.
        group_by_col: Column to group by.
        agg_col: Column to aggregate.
        agg_func: Aggregation function name ('sum', 'avg', 'count', 'min', 'max').
        
    Returns:
        Aggregated DataFrame.
    """
    if df is None or not HAS_PYSPARK:
        return None
    
    agg_functions = {
        'sum': spark_sum(col(agg_col)),
        'avg': avg(col(agg_col)),
        'count': count(col(agg_col)),
    }
    
    agg_func_obj = agg_functions.get(agg_func, spark_sum(col(agg_col)))
    
    return df.groupBy(group_by_col).agg(agg_func_obj.alias(f"{agg_func}_{agg_col}"))


def apply_window_function(df: Any, partition_col: str, order_col: str) -> Any:
    """Apply window function for ranking.
    
    Args:
        df: DataFrame to apply window function to.
        partition_col: Column to partition by.
        order_col: Column to order by.
        
    Returns:
        DataFrame with rank column.
    """
    if df is None or not HAS_PYSPARK:
        return None
    
    window = Window.partitionBy(partition_col).orderBy(col(order_col).desc())
    return df.withColumn("rank", row_number().over(window))


def flatten_data(df: Any, explode_col: str) -> Any:
    """Flatten nested array column using explode.
    
    Args:
        df: DataFrame with array column.
        explode_col: Column name containing arrays.
        
    Returns:
        DataFrame with exploded column.
    """
    if df is None or not HAS_PYSPARK:
        return None
    
    try:
        from pyspark.sql.functions import explode
        return df.select("*", explode(col(explode_col)).alias("flattened"))
    except ImportError:
        return None


def union_dataframes(df1: Any, df2: Any) -> Any:
    """Union two DataFrames.
    
    Args:
        df1: First DataFrame.
        df2: Second DataFrame.
        
    Returns:
        Union of DataFrames.
    """
    if df1 is None or df2 is None or not HAS_PYSPARK:
        return None
    
    return df1.union(df2)