"""Run PySpark transformation examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging
from typing import Any

try:
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, lit
    HAS_PYSPARK = True
except ImportError:
    HAS_PYSPARK = False

from pyspark.transformations.transformations import (
    apply_map_transformation,
    filter_greater_than,
    group_and_aggregate,
    apply_window_function,
    union_dataframes,
)

logger = logging.getLogger(__name__)


def create_sample_spark_df() -> Any:
    """Create sample DataFrame for transformations."""
    if not HAS_PYSPARK:
        return None
    
    spark = SparkSession.builder.appName("Transform-Demo").master("local[*]").getOrCreate()
    
    data = [
        (1, "Alice", 50000.0, "HR"),
        (2, "Bob", 60000.0, "IT"),
        (3, "Charlie", 55000.0, "IT"),
        (4, "Diana", 75000.0, "HR"),
        (5, "Eve", 65000.0, "IT"),
    ]
    
    return spark.createDataFrame(data, ["id", "name", "salary", "dept"])


def run_map_examples() -> None:
    """Demonstrate map transformations."""
    logger.info("Running map transformation examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    df = create_sample_spark_df()
    if df:
        print("Original DataFrame:")
        df.show()

        # Add bonus column (salary * 1.1)
        from pyspark.sql.functions import col
        transformed = df.withColumn("bonus", col("salary") * 0.1)
        print("\nWith bonus column (salary * 0.1):")
        transformed.show()


def run_filter_examples() -> None:
    """Demonstrate filter transformations."""
    logger.info("Running filter examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    df = create_sample_spark_df()
    if df:
        print("Original DataFrame:")
        df.show()

        filtered = filter_greater_than(df, "salary", 55000)
        print("\nFiltered (salary > 55000):")
        if filtered:
            filtered.show()


def run_group_and_aggregate_examples() -> None:
    """Demonstrate groupBy and aggregation."""
    logger.info("Running groupBy and aggregation examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    df = create_sample_spark_df()
    if df:
        print("Original DataFrame:")
        df.show()

        aggregated = group_and_aggregate(df, "dept", "salary", "sum")
        print("\nGrouped by dept with sum of salary:")
        if aggregated:
            aggregated.show()

        avg_agg = group_and_aggregate(df, "dept", "salary", "avg")
        print("\nGrouped by dept with avg salary:")
        if avg_agg:
            avg_agg.show()


def run_window_examples() -> None:
    """Demonstrate window functions."""
    logger.info("Running window function examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    df = create_sample_spark_df()
    if df:
        print("Original DataFrame:")
        df.show()

        windowed = apply_window_function(df, "dept", "salary")
        print("\nWith window ranking (by salary desc within dept):")
        if windowed:
            windowed.show()


def run_union_examples() -> None:
    """Demonstrate union operations."""
    logger.info("Running union examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    spark = SparkSession.builder.appName("Union-Demo").master("local[*]").getOrCreate()

    data1 = [(1, "Alice"), (2, "Bob")]
    data2 = [(3, "Charlie"), (4, "Diana")]

    df1 = spark.createDataFrame(data1, ["id", "name"])
    df2 = spark.createDataFrame(data2, ["id", "name"])

    print("DataFrame 1:")
    df1.show()

    print("\nDataFrame 2:")
    df2.show()

    unioned = union_dataframes(df1, df2)
    print("\nUnioned DataFrames:")
    if unioned:
        unioned.show()


def main() -> None:
    """Main entry point for running examples."""
    parser = argparse.ArgumentParser(description="Run PySpark transformation examples")
    parser.add_argument(
        "--module",
        choices=["map", "filter", "groupby", "window", "union"],
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "map":
        run_map_examples()
    elif args.module == "filter":
        run_filter_examples()
    elif args.module == "groupby":
        run_group_and_aggregate_examples()
    elif args.module == "window":
        run_window_examples()
    elif args.module == "union":
        run_union_examples()
    else:
        # Run all examples
        run_map_examples()
        run_filter_examples()
        run_group_and_aggregate_examples()
        run_window_examples()
        run_union_examples()


if __name__ == "__main__":
    main()