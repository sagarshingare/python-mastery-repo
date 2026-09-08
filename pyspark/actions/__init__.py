"""PySpark actions module.

Exposes eager actions, summary statistics, and distributed file persistence functions.
"""

from __future__ import annotations

from pyspark.actions.actions import (
    HAS_PYSPARK,
    collect_data,
    count_rows,
    get_first_row,
    get_statistics,
    read_storage,
    show_data,
    summarize_dataframe,
    take_rows,
    write_csv,
    write_json,
    write_parquet,
    write_partitioned,
)

__all__ = [
    "HAS_PYSPARK",
    "collect_data",
    "count_rows",
    "get_first_row",
    "get_statistics",
    "read_storage",
    "show_data",
    "summarize_dataframe",
    "take_rows",
    "write_csv",
    "write_json",
    "write_parquet",
    "write_partitioned",
]