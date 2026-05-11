"""Run PySpark basics examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

try:
    from pyspark.sql import SparkSession
    HAS_PYSPARK = True
except ImportError:
    HAS_PYSPARK = False

from pyspark.basics.spark_basics import (
    create_spark_session,
    create_dataframe_from_list,
    create_dataframe_from_dict,
    inspect_dataframe,
    filter_dataframe,
    select_columns,
    sample_data,
)

logger = logging.getLogger(__name__)


def run_create_spark_session_examples() -> None:
    """Demonstrate SparkSession creation."""
    logger.info("Running SparkSession examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    spark = create_spark_session("Demo-App")
    if spark:
        print(f"SparkSession created: {spark.appName}")
        print(f"Spark version: {spark.version}")
    else:
        print("Failed to create SparkSession")


def run_create_dataframe_examples() -> None:
    """Demonstrate DataFrame creation."""
    logger.info("Running DataFrame creation examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    spark = create_spark_session("DataFrame-Demo")
    if not spark:
        return

    # From list
    data = sample_data()
    print(f"\nSample data: {data}")

    df = create_dataframe_from_list(spark, data, ["id", "name", "salary"])
    if df:
        print("\nDataFrame created from list:")
        df.show()

    # From dict
    dict_data = [
        {"id": 1, "name": "Alice", "salary": 50000.0},
        {"id": 2, "name": "Bob", "salary": 60000.0},
    ]
    df_dict = create_dataframe_from_dict(spark, dict_data)
    if df_dict:
        print("\nDataFrame created from dict:")
        df_dict.show()


def run_inspect_dataframe_examples() -> None:
    """Demonstrate DataFrame inspection."""
    logger.info("Running DataFrame inspection examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    spark = create_spark_session("Inspect-Demo")
    if not spark:
        return

    data = sample_data()
    df = create_dataframe_from_list(spark, data, ["id", "name", "salary"])

    if df:
        metadata = inspect_dataframe(df)
        print(f"\nDataFrame metadata:")
        for key, value in metadata.items():
            print(f"  {key}: {value}")


def run_filter_examples() -> None:
    """Demonstrate DataFrame filtering."""
    logger.info("Running DataFrame filter examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    spark = create_spark_session("Filter-Demo")
    if not spark:
        return

    data = sample_data()
    df = create_dataframe_from_list(spark, data, ["id", "name", "salary"])

    if df:
        print("\nOriginal DataFrame:")
        df.show()

        filtered = filter_dataframe(df, "salary > 55000")
        print("\nFiltered (salary > 55000):")
        if filtered:
            filtered.show()


def run_select_examples() -> None:
    """Demonstrate column selection."""
    logger.info("Running DataFrame select examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    spark = create_spark_session("Select-Demo")
    if not spark:
        return

    data = sample_data()
    df = create_dataframe_from_list(spark, data, ["id", "name", "salary"])

    if df:
        print("\nOriginal DataFrame:")
        df.show()

        selected = select_columns(df, ["name", "salary"])
        print("\nSelected columns (name, salary):")
        if selected:
            selected.show()


def main() -> None:
    """Main entry point for running examples."""
    parser = argparse.ArgumentParser(description="Run PySpark basics examples")
    parser.add_argument(
        "--module",
        choices=["spark_session", "dataframe", "inspect", "filter", "select"],
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "spark_session":
        run_create_spark_session_examples()
    elif args.module == "dataframe":
        run_create_dataframe_examples()
    elif args.module == "inspect":
        run_inspect_dataframe_examples()
    elif args.module == "filter":
        run_filter_examples()
    elif args.module == "select":
        run_select_examples()
    else:
        # Run all examples
        run_create_spark_session_examples()
        run_create_dataframe_examples()
        run_inspect_dataframe_examples()
        run_filter_examples()
        run_select_examples()


if __name__ == "__main__":
    main()