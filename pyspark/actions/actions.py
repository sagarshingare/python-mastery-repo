"""PySpark actions - collect, count, take, summary, and distributed file sinks.

This module demonstrates PySpark action concepts and persistence patterns:
- Eager Actions: collect (driver retrieval), count, take, first, head
- DataFrame Summary: describe / summary statistical profiling
- Distributed File Sinks: Parquet, CSV, and JSON persistence
- Partitioned Writes: Directory-based partition pruning (e.g. partitionBy("dept"))
- Round-Trip Ingestion: Reading persisted Parquet datasets back into DataFrames

Python version: 3.9+
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

try:
    from pyspark.sql import DataFrame, SparkSession
    HAS_PYSPARK = True
except ImportError:  # pragma: no cover
    HAS_PYSPARK = False
    DataFrame = Any  # type: ignore[misc, assignment]

logger = logging.getLogger(__name__)


def collect_data(df: Optional[DataFrame]) -> List[Tuple[Any, ...]]:
    """Collect all DataFrame rows to driver memory as Python tuples.

    Caution: In production clusters, only call .collect() on filtered or aggregated data
    to prevent Driver Out-Of-Memory (OOM) errors.

    Args:
        df: DataFrame to collect.

    Returns:
        List of rows formatted as standard Python tuples.
    """
    if df is None or not HAS_PYSPARK:
        return []

    try:
        rows = df.collect()
        return [tuple(row) for row in rows]
    except Exception as exc:
        logger.error("Error collecting DataFrame data: %s", exc)
        return []


def count_rows(df: Optional[DataFrame]) -> int:
    """Count total rows in a DataFrame (triggers an action job).

    Args:
        df: DataFrame to count.

    Returns:
        Total row count.
    """
    if df is None or not HAS_PYSPARK:
        return 0

    try:
        return df.count()
    except Exception as exc:
        logger.error("Error counting rows: %s", exc)
        return 0


def get_first_row(df: Optional[DataFrame]) -> Optional[Tuple[Any, ...]]:
    """Get the first row from a DataFrame.

    Args:
        df: DataFrame.

    Returns:
        First row as a tuple, or None if empty.
    """
    if df is None or not HAS_PYSPARK:
        return None

    try:
        first = df.first()
        return tuple(first) if first else None
    except Exception as exc:
        logger.error("Error retrieving first row: %s", exc)
        return None


def take_rows(df: Optional[DataFrame], n: int = 5) -> List[Tuple[Any, ...]]:
    """Take the first n rows from the DataFrame without collecting the full dataset.

    Args:
        df: Source DataFrame.
        n: Number of records to retrieve.

    Returns:
        List of n rows formatted as tuples.
    """
    if df is None or not HAS_PYSPARK:
        return []

    try:
        rows = df.take(n)
        return [tuple(row) for row in rows]
    except Exception as exc:
        logger.error("Error taking rows: %s", exc)
        return []


def show_data(df: Optional[DataFrame], num_rows: int = 5, truncate: bool = True) -> None:
    """Print formatted DataFrame contents to standard output.

    Args:
        df: DataFrame to display.
        num_rows: Number of rows to show.
        truncate: Whether to truncate strings > 20 chars.
    """
    if df is None or not HAS_PYSPARK:
        print("DataFrame is None or PySpark is not available.")
        return

    try:
        df.show(num_rows, truncate=truncate)
    except Exception as exc:
        logger.error("Error displaying DataFrame: %s", exc)


def summarize_dataframe(df: Optional[DataFrame]) -> Optional[DataFrame]:
    """Generate statistical summary metrics (count, mean, stddev, min, 25%, 50%, 75%, max).

    Args:
        df: DataFrame to profile.

    Returns:
        Summary metrics DataFrame.
    """
    if df is None or not HAS_PYSPARK:
        return None

    try:
        return df.summary()
    except Exception as exc:
        logger.error("Error generating DataFrame summary: %s", exc)
        return None


def write_parquet(
    df: Optional[DataFrame],
    path: str,
    mode: str = "overwrite",
    compression: str = "snappy",
) -> bool:
    """Persist DataFrame in column-oriented Parquet format with Snappy compression.

    Args:
        df: DataFrame to write.
        path: Output directory path.
        mode: Save mode ('overwrite', 'append', 'ignore', 'errorIfExists').
        compression: Parquet compression codec (default 'snappy').

    Returns:
        True if write succeeded, False otherwise.
    """
    if df is None or not HAS_PYSPARK:
        return False

    try:
        df.write.mode(mode).option("compression", compression).parquet(path)
        return True
    except Exception as exc:
        logger.error("Error writing Parquet: %s", exc)
        return False


def write_partitioned(
    df: Optional[DataFrame],
    path: str,
    partition_cols: List[str],
    file_format: str = "parquet",
    mode: str = "overwrite",
) -> bool:
    """Write DataFrame partitioned into subdirectories (e.g., path/dept=HR/).

    Args:
        df: DataFrame to write.
        path: Base output directory.
        partition_cols: Columns used to partition files.
        file_format: Storage format ('parquet', 'csv', 'json').
        mode: Write mode.

    Returns:
        True if write succeeded, False otherwise.
    """
    if df is None or not HAS_PYSPARK:
        return False

    try:
        writer = df.write.mode(mode).partitionBy(*partition_cols)
        if file_format.lower() == "parquet":
            writer.parquet(path)
        elif file_format.lower() == "csv":
            writer.option("header", True).csv(path)
        elif file_format.lower() == "json":
            writer.json(path)
        else:
            writer.format(file_format).save(path)
        return True
    except Exception as exc:
        logger.error("Error writing partitioned data: %s", exc)
        return False


def write_csv(
    df: Optional[DataFrame],
    path: str,
    mode: str = "overwrite",
    header: bool = True,
) -> bool:
    """Persist DataFrame to CSV format.

    Args:
        df: DataFrame to write.
        path: Output directory path.
        mode: Save mode.
        header: Whether to include CSV header.

    Returns:
        True if write succeeded, False otherwise.
    """
    if df is None or not HAS_PYSPARK:
        return False

    try:
        df.write.mode(mode).option("header", header).csv(path)
        return True
    except Exception as exc:
        logger.error("Error writing CSV: %s", exc)
        return False


def write_json(df: Optional[DataFrame], path: str, mode: str = "overwrite") -> bool:
    """Persist DataFrame to newline-delimited JSON format.

    Args:
        df: DataFrame to write.
        path: Output directory path.
        mode: Save mode.

    Returns:
        True if write succeeded, False otherwise.
    """
    if df is None or not HAS_PYSPARK:
        return False

    try:
        df.write.mode(mode).json(path)
        return True
    except Exception as exc:
        logger.error("Error writing JSON: %s", exc)
        return False


def read_storage(
    spark: Optional[SparkSession],
    path: str,
    file_format: str = "parquet",
) -> Optional[DataFrame]:
    """Read persisted files from disk back into a DataFrame.

    Args:
        spark: Active SparkSession.
        path: Storage directory path.
        file_format: 'parquet', 'csv', 'json'.

    Returns:
        Loaded DataFrame or None.
    """
    if spark is None or not HAS_PYSPARK:
        return None

    try:
        if file_format.lower() == "parquet":
            return spark.read.parquet(path)
        elif file_format.lower() == "csv":
            return spark.read.option("header", True).option("inferSchema", True).csv(path)
        elif file_format.lower() == "json":
            return spark.read.json(path)
        return spark.read.format(file_format).load(path)
    except Exception as exc:
        logger.error("Error reading storage from %s: %s", path, exc)
        return None


def get_statistics(df: Optional[DataFrame]) -> Dict[str, Any]:
    """Get metadata and schema statistics for a DataFrame.

    Args:
        df: DataFrame to inspect.

    Returns:
        Dictionary with row_count, column_count, columns, and dtypes.
    """
    if df is None or not HAS_PYSPARK:
        return {}

    try:
        return {
            "row_count": df.count(),
            "column_count": len(df.columns),
            "columns": df.columns,
            "dtypes": df.dtypes,
        }
    except Exception as exc:
        logger.error("Error getting statistics: %s", exc)
        return {}