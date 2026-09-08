"""Run PySpark action and file sink examples with a comprehensive CLI."""

from __future__ import annotations

import argparse
import logging
import os
import tempfile
from typing import Optional

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
from pyspark.basics.spark_basics import (
    create_spark_session,
    stop_spark_session,
)

logger = logging.getLogger(__name__)


def create_sample_dataset(spark: object) -> object:
    """Create sample sales/employee records for action demonstrations."""
    data = [
        (1, "Alice", 95000.0, "Engineering", "East"),
        (2, "Bob", 62000.0, "Marketing", "West"),
        (3, "Charlie", 110000.0, "Engineering", "East"),
        (4, "Diana", 88000.0, "Product", "West"),
        (5, "Evan", 105000.0, "Engineering", "Central"),
        (6, "Fiona", 74000.0, "Marketing", "Central"),
    ]
    return spark.createDataFrame(data, ["id", "name", "salary", "dept", "region"])


def run_collect_demo(df: object) -> None:
    """Demonstrate collect action vs take action."""
    print("\n--- 1. Collect Action vs Take (Driver Memory Management) ---")
    first_row = get_first_row(df)
    print(f"First Row: {first_row}")

    top3 = take_rows(df, 3)
    print("Take First 3 Rows (Safe for Large Datasets):")
    for row in top3:
        print(f"  {row}")

    print("Full Collection to Driver (Caution on multi-GB tables):")
    all_rows = collect_data(df)
    print(f"Collected total {len(all_rows)} rows.")


def run_count_demo(df: object) -> None:
    """Demonstrate count action."""
    print("\n--- 2. Count Action ---")
    row_count = count_rows(df)
    print(f"Total row count in DataFrame: {row_count}")


def run_summary_demo(df: object) -> None:
    """Demonstrate statistical summary profiling."""
    print("\n--- 3. Statistical Summary Profiling (.summary()) ---")
    summary = summarize_dataframe(df)
    if summary:
        summary.show()


def run_write_demo(df: object) -> None:
    """Demonstrate multi-format file writes (Parquet, CSV, JSON)."""
    print("\n--- 4. Multi-Format File Persistence ---")
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_path = os.path.join(tmpdir, "employees.parquet")
        csv_path = os.path.join(tmpdir, "employees.csv")
        json_path = os.path.join(tmpdir, "employees.json")

        if write_parquet(df, parquet_path):
            print(f"✓ Wrote Parquet (Snappy-compressed) to: {parquet_path}")

        if write_csv(df, csv_path):
            print(f"✓ Wrote CSV with headers to:             {csv_path}")

        if write_json(df, json_path):
            print(f"✓ Wrote newline-delimited JSON to:      {json_path}")


def run_partition_demo(spark: object, df: object) -> None:
    """Demonstrate partitioned writes and round-trip read with partition discovery."""
    print("\n--- 5. Partitioned Sinks & Read-Back ---")
    with tempfile.TemporaryDirectory() as tmpdir:
        partition_path = os.path.join(tmpdir, "partitioned_by_dept")
        print(f"Writing dataset partitioned by 'dept' to: {partition_path}")

        success = write_partitioned(df, partition_path, partition_cols=["dept"], file_format="parquet")
        if success:
            print("✓ Partition write succeeded.")
            print("Directory structure created by Spark:")
            for root, dirs, files in os.walk(partition_path):
                level = root.replace(partition_path, "").count(os.sep)
                indent = " " * 4 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = " " * 4 * (level + 1)
                for f in files:
                    if f.endswith(".parquet"):
                        print(f"{subindent}{f}")

            # Round-trip read back
            reloaded = read_storage(spark, partition_path, file_format="parquet")
            if reloaded:
                print("\nReloaded DataFrame from partitioned Parquet (Spark auto-infers partition columns):")
                reloaded.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PySpark action demonstrations")
    parser.add_argument(
        "--demo",
        "--module",
        dest="demo",
        choices=["collect", "count", "take", "show", "summary", "write", "partition", "all"],
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

    spark = create_spark_session("Actions-Master-Demo")
    try:
        df = create_sample_dataset(spark)
        if args.demo in ("all", "collect", "take"):
            run_collect_demo(df)
        if args.demo in ("all", "count"):
            run_count_demo(df)
        if args.demo in ("all", "show"):
            print("\n--- Display Action (.show()) ---")
            show_data(df, num_rows=5, truncate=False)
        if args.demo in ("all", "summary"):
            run_summary_demo(df)
        if args.demo in ("all", "write"):
            run_write_demo(df)
        if args.demo in ("all", "partition"):
            run_partition_demo(spark, df)
    finally:
        stop_spark_session(spark)


if __name__ == "__main__":
    main()