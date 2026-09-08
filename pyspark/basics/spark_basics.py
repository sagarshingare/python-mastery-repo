"""PySpark basics - SparkSession, DataFrames, and fundamental operations."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

try:
    from pyspark.sql import DataFrame, SparkSession
    from pyspark.sql.types import (
        DoubleType,
        IntegerType,
        StringType,
        StructField,
        StructType,
    )
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


def create_spark_session(app_name: str = "PySpark-Basics", master: str = "local[1]") -> Optional[SparkSession]:
    """Create and return a configured local SparkSession."""
    if not HAS_PYSPARK or SparkSession is None:
        logger.warning("PySpark is not installed or available.")
        return None

    try:
        spark = (
            SparkSession.builder
            .appName(app_name)
            .master(master)
            .config("spark.ui.enabled", "false")
            .config("spark.sql.shuffle.partitions", "2")
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("WARN")
        return spark
    except Exception as exc:
        logger.error("Failed to initialize SparkSession: %s", exc)
        return None


def stop_spark_session(spark: Optional[SparkSession]) -> None:
    """Safely stop an active SparkSession."""
    if spark is not None:
        try:
            spark.stop()
        except Exception as exc:
            logger.debug("Error while stopping SparkSession: %s", exc)


def create_dataframe_from_list(
    spark: Optional[SparkSession],
    data: List[tuple],
    schema: List[str] | StructType,
) -> Optional[DataFrame]:
    """Create a DataFrame from a list of tuples with given schema."""
    if spark is None:
        return None
    return spark.createDataFrame(data, schema=schema)


def create_dataframe_from_dict(
    spark: Optional[SparkSession],
    data: List[Dict[str, Any]],
) -> Optional[DataFrame]:
    """Create a DataFrame from a list of dictionaries."""
    if spark is None:
        return None
    return spark.createDataFrame(data)


def define_custom_schema() -> Optional[StructType]:
    """Define a strongly-typed StructType schema for employee records."""
    if not HAS_PYSPARK or StructType is None:
        return None

    return StructType([
        StructField("id", IntegerType(), nullable=False),
        StructField("name", StringType(), nullable=True),
        StructField("department", StringType(), nullable=True),
        StructField("salary", DoubleType(), nullable=True),
    ])


def inspect_dataframe(df: Optional[DataFrame]) -> Dict[str, Any]:
    """Inspect a DataFrame and extract schema and size metadata."""
    if df is None:
        return {}

    return {
        "columns": df.columns,
        "column_count": len(df.columns),
        "row_count": df.count(),
        "schema_fields": [f.name for f in df.schema.fields],
        "dtypes": df.dtypes,
    }


def filter_dataframe(df: Optional[DataFrame], condition: str) -> Optional[DataFrame]:
    """Filter rows of a DataFrame using an expression condition."""
    if df is None:
        return None
    return df.filter(condition)


def select_columns(df: Optional[DataFrame], columns: List[str]) -> Optional[DataFrame]:
    """Select specific columns from a DataFrame."""
    if df is None:
        return None
    return df.select(*columns)


def sample_data() -> List[Tuple[int, str, str, float]]:
    """Return sample employee records (id, name, department, salary)."""
    return [
        (1, "Alice", "Engineering", 95000.0),
        (2, "Bob", "Marketing", 62000.0),
        (3, "Charlie", "Engineering", 110000.0),
        (4, "Diana", "Product", 88000.0),
        (5, "Evan", "Engineering", 105000.0),
    ]