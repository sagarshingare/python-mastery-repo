"""PySpark basics module.

Exposes core SparkSession creation, schema definition, DataFrame ingestion,
inspection, and filtering primitives.
"""

from __future__ import annotations

from pyspark.basics.spark_basics import (
    HAS_PYSPARK,
    create_dataframe_from_dict,
    create_dataframe_from_list,
    create_spark_session,
    define_custom_schema,
    filter_dataframe,
    inspect_dataframe,
    sample_data,
    select_columns,
    stop_spark_session,
)

__all__ = [
    "HAS_PYSPARK",
    "create_dataframe_from_dict",
    "create_dataframe_from_list",
    "create_spark_session",
    "define_custom_schema",
    "filter_dataframe",
    "inspect_dataframe",
    "sample_data",
    "select_columns",
    "stop_spark_session",
]