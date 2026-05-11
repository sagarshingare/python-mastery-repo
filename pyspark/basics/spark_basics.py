"""PySpark basics - DataFrames, RDDs, and fundamental operations.

This module demonstrates core PySpark concepts including:
- SparkSession initialization and configuration
- Creating DataFrames from various sources
- Basic DataFrame operations
- Schema definition and manipulation
- DataFrame display and inspection

Python version: 3.9+
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from pyspark.sql import SparkSession, DataFrame
else:
    SparkSession = Any  # type: ignore
    DataFrame = Any  # type: ignore

try:
    from pyspark.sql import SparkSession, DataFrame
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
    HAS_PYSPARK = True
except ImportError:
    HAS_PYSPARK = False
    SparkSession = None  # type: ignore
    DataFrame = None  # type: ignore
    StructType = None  # type: ignore
    StructField = None  # type: ignore
    StringType = None  # type: ignore
    IntegerType = None  # type: ignore
    DoubleType = None  # type: ignore
    StructType = None  # type: ignore


def create_spark_session(app_name: str = "PySpark-Basics") -> Any:
    """Create and return a SparkSession.
    
    Args:
        app_name: Name of the Spark application.
        
    Returns:
        SparkSession instance or None if PySpark is not installed.
    """
    if SparkSession is None:
        return None
    
    return (SparkSession.builder
            .appName(app_name)
            .master("local[*]")
            .getOrCreate())


def create_dataframe_from_list(spark: Any, 
                               data: List[tuple],
                               schema: List[str]) -> Any:
    """Create a DataFrame from a list of tuples.
    
    Args:
        spark: SparkSession instance.
        data: List of tuples representing rows.
        schema: List of column names.
        
    Returns:
        DataFrame or None if spark is None.
    """
    if spark is None:
        return None
    
    return spark.createDataFrame(data, schema=schema)


def create_dataframe_from_dict(spark: Any,
                               data: List[Dict[str, Any]]) -> Any:
    """Create a DataFrame from a list of dictionaries.
    
    Args:
        spark: SparkSession instance.
        data: List of dictionaries.
        
    Returns:
        DataFrame or None if spark is None.
    """
    if spark is None:
        return None
    
    return spark.createDataFrame(data)


def define_custom_schema() -> Any:
    """Define a custom schema for a DataFrame.
    
    Returns:
        StructType schema or None if PySpark is not installed.
    """
    if StructType is None:
        return None
    
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("salary", DoubleType(), True),
    ])
    
    return schema


def inspect_dataframe(df: Any) -> Dict[str, Any]:
    """Inspect a DataFrame and return metadata.
    
    Args:
        df: DataFrame to inspect.
        
    Returns:
        Dictionary containing DataFrame metadata.
    """
    if df is None:
        return {}
    
    return {
        "columns": df.columns,
        "row_count": df.count(),
        "schema": str(df.schema),
        "dtypes": df.dtypes,
    }


def filter_dataframe(df: Any, condition: str) -> Any:
    """Filter a DataFrame based on a condition.
    
    Args:
        df: DataFrame to filter.
        condition: SQL-like condition string.
        
    Returns:
        Filtered DataFrame or None.
    """
    if df is None:
        return None
    
    return df.filter(condition)


def select_columns(df: Any, columns: List[str]) -> Any:
    """Select specific columns from a DataFrame.
    
    Args:
        df: DataFrame to select from.
        columns: List of column names to select.
        
    Returns:
        DataFrame with selected columns or None.
    """
    if df is None:
        return None
    
    return df.select(columns)


def sample_data() -> List[tuple]:
    """Get sample employee data.
    
    Returns:
        List of employee tuples.
    """
    return [
        (1, "Alice", 50000.0),
        (2, "Bob", 60000.0),
        (3, "Charlie", 55000.0),
        (4, "Diana", 75000.0),
        (5, "Eve", 65000.0),
    ]