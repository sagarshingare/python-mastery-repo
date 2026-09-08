"""Run PySpark basics examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging
from typing import Optional

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

logger = logging.getLogger(__name__)


def run_create_spark_session_examples(spark: Optional[object] = None) -> None:
    """Demonstrate SparkSession creation."""
    print("--- 1. SparkSession Initialization ---")
    if not HAS_PYSPARK:
        print("PySpark is not installed. Skipping demo.")
        return

    local_spark = spark or create_spark_session("Session-Demo")
    if local_spark:
        print(f"  App Name:      {local_spark.sparkContext.appName}")
        print(f"  Spark Version: {local_spark.version}")
        print(f"  Master URL:    {local_spark.sparkContext.master}")
        if spark is None:
            stop_spark_session(local_spark)
    else:
        print("Failed to create SparkSession.")


def run_create_dataframe_examples(spark: Optional[object] = None) -> None:
    """Demonstrate DataFrame creation from lists and dictionaries."""
    print("\n--- 2. DataFrame Ingestion (List & Dict) ---")
    if not HAS_PYSPARK:
        print("PySpark is not installed. Skipping demo.")
        return

    local_spark = spark or create_spark_session("DataFrame-Demo")
    if not local_spark:
        return

    # From typed list with custom schema
    schema = define_custom_schema()
    data = sample_data()
    df_list = create_dataframe_from_list(local_spark, data, schema=schema)
    if df_list:
        print("DataFrame from List (Strongly Typed Schema):")
        df_list.show()

    # From dicts
    dict_data = [
        {"id": 101, "name": "Fiona", "department": "Design", "salary": 72000.0},
        {"id": 102, "name": "George", "department": "Design", "salary": 78000.0},
    ]
    df_dict = create_dataframe_from_dict(local_spark, dict_data)
    if df_dict:
        print("DataFrame from Dictionaries:")
        df_dict.show()

    if spark is None:
        stop_spark_session(local_spark)


def run_inspect_dataframe_examples(spark: Optional[object] = None) -> None:
    """Demonstrate DataFrame schema and metadata inspection."""
    print("\n--- 3. Schema & Metadata Inspection ---")
    if not HAS_PYSPARK:
        return

    local_spark = spark or create_spark_session("Inspect-Demo")
    if not local_spark:
        return

    df = create_dataframe_from_list(local_spark, sample_data(), define_custom_schema())
    if df:
        meta = inspect_dataframe(df)
        print(f"  Row Count: {meta['row_count']}")
        print(f"  Columns:   {meta['columns']}")
        print(f"  DataTypes: {meta['dtypes']}")

    if spark is None:
        stop_spark_session(local_spark)


def run_filter_examples(spark: Optional[object] = None) -> None:
    """Demonstrate DataFrame row filtering."""
    print("\n--- 4. DataFrame Filtering ---")
    if not HAS_PYSPARK:
        return

    local_spark = spark or create_spark_session("Filter-Demo")
    if not local_spark:
        return

    df = create_dataframe_from_list(local_spark, sample_data(), define_custom_schema())
    if df:
        print("Employees with salary >= $90,000:")
        filtered = filter_dataframe(df, "salary >= 90000")
        if filtered:
            filtered.show()

    if spark is None:
        stop_spark_session(local_spark)


def run_select_examples(spark: Optional[object] = None) -> None:
    """Demonstrate column selection and projection."""
    print("\n--- 5. Column Selection & Projection ---")
    if not HAS_PYSPARK:
        return

    local_spark = spark or create_spark_session("Select-Demo")
    if not local_spark:
        return

    df = create_dataframe_from_list(local_spark, sample_data(), define_custom_schema())
    if df:
        print("Projected columns [name, salary]:")
        selected = select_columns(df, ["name", "salary"])
        if selected:
            selected.show()

    if spark is None:
        stop_spark_session(local_spark)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PySpark basics demonstrations")
    parser.add_argument(
        "--demo",
        choices=["session", "dataframe", "inspect", "filter", "select", "all"],
        default="all",
        help="Demonstration to run (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if not HAS_PYSPARK:
        print("PySpark is not installed. Please install pyspark to run live demos.")
        return

    # Use a single shared SparkSession for the entire demo run
    spark = create_spark_session("Basics-Master-Demo")
    try:
        if args.demo in ("all", "session"):
            run_create_spark_session_examples(spark)
        if args.demo in ("all", "dataframe"):
            run_create_dataframe_examples(spark)
        if args.demo in ("all", "inspect"):
            run_inspect_dataframe_examples(spark)
        if args.demo in ("all", "filter"):
            run_filter_examples(spark)
        if args.demo in ("all", "select"):
            run_select_examples(spark)
    finally:
        stop_spark_session(spark)


if __name__ == "__main__":
    main()