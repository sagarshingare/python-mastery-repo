"""Run PySpark action examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging
from typing import Any

try:
    from pyspark.sql import SparkSession
    HAS_PYSPARK = True
except ImportError:
    HAS_PYSPARK = False

from pyspark.actions.actions import (
    collect_data,
    count_rows,
    get_first_row,
    take_rows,
    show_data,
    foreach_row,
    write_parquet,
    write_csv,
    write_json,
    get_statistics,
)

logger = logging.getLogger(__name__)


def create_sample_spark_df() -> Any:
    """Create sample DataFrame for action examples."""
    if not HAS_PYSPARK:
        return None
    
    spark = SparkSession.builder.appName("Actions-Demo").master("local[*]").getOrCreate()
    
    data = [
        (1, "Alice", 50000.0, "HR"),
        (2, "Bob", 60000.0, "IT"),
        (3, "Charlie", 55000.0, "IT"),
        (4, "Diana", 75000.0, "HR"),
        (5, "Eve", 65000.0, "IT"),
    ]
    
    return spark.createDataFrame(data, ["id", "name", "salary", "dept"])


def run_collect_examples() -> None:
    """Demonstrate collect action."""
    logger.info("Running collect examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    df = create_sample_spark_df()
    if df:
        print("Collecting all data to driver:")
        data = collect_data(df)
        print(f"Collected {len(data)} rows:")
        for row in data:
            print(f"  {row}")


def run_count_examples() -> None:
    """Demonstrate count action."""
    logger.info("Running count examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    df = create_sample_spark_df()
    if df:
        row_count = count_rows(df)
        print(f"Total rows in DataFrame: {row_count}")


def run_first_examples() -> None:
    """Demonstrate first and take actions."""
    logger.info("Running first and take examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    df = create_sample_spark_df()
    if df:
        first_row = get_first_row(df)
        print(f"First row: {first_row}")

        taken_rows = take_rows(df, 3)
        print(f"\nFirst 3 rows:")
        for row in taken_rows:
            print(f"  {row}")


def run_show_examples() -> None:
    """Demonstrate show action."""
    logger.info("Running show examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    df = create_sample_spark_df()
    if df:
        print("Formatted DataFrame display:")
        show_data(df, num_rows=5, truncate=False)


def run_foreach_examples() -> None:
    """Demonstrate foreach action."""
    logger.info("Running foreach examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    df = create_sample_spark_df()
    if df:
        print("Processing each row with foreach:")
        
        def process_row(row: Any) -> None:
            """Process a single row."""
            print(f"  Processing: {row['name']} with salary {row['salary']}")
        
        count = foreach_row(df, process_row)
        print(f"Processed {count} rows")


def run_statistics_examples() -> None:
    """Demonstrate statistics action."""
    logger.info("Running statistics examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    df = create_sample_spark_df()
    if df:
        stats = get_statistics(df)
        print("DataFrame Statistics:")
        print(f"  Row count: {stats.get('row_count', 'N/A')}")
        print(f"  Column count: {stats.get('column_count', 'N/A')}")
        print(f"  Columns: {stats.get('columns', [])}")
        print(f"  Data types:")
        for col_name, dtype in stats.get('dtypes', []):
            print(f"    {col_name}: {dtype}")


def run_write_examples() -> None:
    """Demonstrate write actions."""
    logger.info("Running write examples")

    if not HAS_PYSPARK:
        print("PySpark not installed. Skipping examples.")
        return

    df = create_sample_spark_df()
    if df:
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"Writing DataFrame to temporary directory: {tmpdir}")
            
            # Write Parquet
            parquet_path = os.path.join(tmpdir, "data.parquet")
            if write_parquet(df, parquet_path):
                print(f"✓ Successfully wrote Parquet to {parquet_path}")
            
            # Write CSV
            csv_path = os.path.join(tmpdir, "data.csv")
            if write_csv(df, csv_path):
                print(f"✓ Successfully wrote CSV to {csv_path}")
            
            # Write JSON
            json_path = os.path.join(tmpdir, "data.json")
            if write_json(df, json_path):
                print(f"✓ Successfully wrote JSON to {json_path}")


def main() -> None:
    """Main entry point for running examples."""
    parser = argparse.ArgumentParser(description="Run PySpark action examples")
    parser.add_argument(
        "--module",
        choices=["collect", "count", "first", "show", "foreach", "statistics", "write"],
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "collect":
        run_collect_examples()
    elif args.module == "count":
        run_count_examples()
    elif args.module == "first":
        run_first_examples()
    elif args.module == "show":
        run_show_examples()
    elif args.module == "foreach":
        run_foreach_examples()
    elif args.module == "statistics":
        run_statistics_examples()
    elif args.module == "write":
        run_write_examples()
    else:
        # Run all examples
        run_collect_examples()
        run_count_examples()
        run_first_examples()
        run_show_examples()
        run_foreach_examples()
        run_statistics_examples()
        run_write_examples()


if __name__ == "__main__":
    main()