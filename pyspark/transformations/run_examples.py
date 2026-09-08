"""Run PySpark transformation examples with a comprehensive CLI."""

from __future__ import annotations

import argparse
import logging
from typing import Optional

from pyspark.basics.spark_basics import (
    create_spark_session,
    stop_spark_session,
)
from pyspark.transformations.transformations import (
    HAS_PYSPARK,
    apply_map_transformation,
    apply_window_analytics,
    apply_window_function,
    broadcast_join,
    derive_columns,
    filter_greater_than,
    group_and_aggregate,
    join_dataframes,
    union_dataframes,
)

logger = logging.getLogger(__name__)


def create_employee_dataset(spark: object) -> object:
    """Create a sample employee dataset for transformation demos."""
    data = [
        (1, "Alice", "Engineering", 95000.0),
        (2, "Bob", "Marketing", 62000.0),
        (3, "Charlie", "Engineering", 110000.0),
        (4, "Diana", "Product", 88000.0),
        (5, "Evan", "Engineering", 105000.0),
        (6, "Fiona", "Marketing", 75000.0),
    ]
    return spark.createDataFrame(data, ["id", "name", "dept", "salary"])


def create_department_dataset(spark: object) -> object:
    """Create a small dimension department table for join demos."""
    data = [
        ("Engineering", "Building A", "Tech"),
        ("Marketing", "Building B", "Business"),
        ("Product", "Building A", "Product"),
        ("Legal", "Building C", "Corporate"),
    ]
    return spark.createDataFrame(data, ["dept", "location", "division"])


def run_map_demo(spark: object) -> None:
    """Demonstrate narrow column mapping and arithmetic."""
    print("\n--- 1. Narrow Mapping & Column Derivation ---")
    df = create_employee_dataset(spark)
    print("Original Employees:")
    df.show()

    derived = derive_columns(df)
    if derived:
        print("With Derived Columns (bonus, total_comp, tier):")
        derived.select("name", "dept", "salary", "bonus", "total_comp", "tier").show()


def run_filter_demo(spark: object) -> None:
    """Demonstrate narrow filter transformations."""
    print("\n--- 2. Narrow Filtering (Predicate Pushdown Capable) ---")
    df = create_employee_dataset(spark)
    filtered = filter_greater_than(df, "salary", 80000.0)
    if filtered:
        print("Employees with salary > $80,000:")
        filtered.show()


def run_groupby_demo(spark: object) -> None:
    """Demonstrate wide transformations (groupBy aggregation requiring shuffle)."""
    print("\n--- 3. Wide Aggregations (Shuffle Required) ---")
    df = create_employee_dataset(spark)

    print("Department Total Salary:")
    agg_sum = group_and_aggregate(df, "dept", "salary", "sum")
    if agg_sum:
        agg_sum.show()

    print("Department Average Salary:")
    agg_avg = group_and_aggregate(df, "dept", "salary", "avg")
    if agg_avg:
        agg_avg.show()


def run_join_demo(spark: object) -> None:
    """Demonstrate standard inner and left joins."""
    print("\n--- 4. DataFrame Joins ---")
    emp_df = create_employee_dataset(spark)
    dept_df = create_department_dataset(spark)

    print("Inner Join (Employees & Departments):")
    joined = join_dataframes(emp_df, dept_df, join_key="dept", how="inner")
    if joined:
        joined.select("id", "name", "dept", "location", "division").show()


def run_broadcast_demo(spark: object) -> None:
    """Demonstrate optimized Broadcast Hash Join for dimension tables."""
    print("\n--- 5. Broadcast Hash Join (Zero Shuffle for Lookup Table) ---")
    emp_df = create_employee_dataset(spark)
    dept_df = create_department_dataset(spark)

    broadcasted = broadcast_join(emp_df, dept_df, join_key="dept", how="left")
    if broadcasted:
        print("Broadcast Join Result:")
        broadcasted.select("name", "dept", "salary", "location").show()


def run_window_demo(spark: object) -> None:
    """Demonstrate analytical window functions (ranking and cumulative sum)."""
    print("\n--- 6. Window Analytics (Rank & Running Total) ---")
    df = create_employee_dataset(spark)

    print("Rank within Department by Salary Descending:")
    ranked = apply_window_function(df, partition_col="dept", order_col="salary")
    if ranked:
        ranked.show()

    print("Advanced Window: Dense Rank and Cumulative Running Total:")
    advanced = apply_window_analytics(df, partition_col="dept", order_col="salary", value_col="salary")
    if advanced:
        advanced.show()


def run_union_demo(spark: object) -> None:
    """Demonstrate unioning two DataFrames."""
    print("\n--- 7. DataFrame Union ---")
    data_cohort_a = [(101, "Grace", "Engineering", 99000.0)]
    data_cohort_b = [(102, "Hank", "Product", 87000.0)]

    df_a = spark.createDataFrame(data_cohort_a, ["id", "name", "dept", "salary"])
    df_b = spark.createDataFrame(data_cohort_b, ["id", "name", "dept", "salary"])

    unioned = union_dataframes(df_a, df_b)
    if unioned:
        print("Unioned Cohorts:")
        unioned.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PySpark transformation demonstrations")
    parser.add_argument(
        "--demo",
        "--module",
        dest="demo",
        choices=["map", "filter", "derive", "groupby", "join", "broadcast", "window", "union", "all"],
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

    spark = create_spark_session("Transformations-Master-Demo")
    try:
        if args.demo in ("all", "map", "derive"):
            run_map_demo(spark)
        if args.demo in ("all", "filter"):
            run_filter_demo(spark)
        if args.demo in ("all", "groupby"):
            run_groupby_demo(spark)
        if args.demo in ("all", "join"):
            run_join_demo(spark)
        if args.demo in ("all", "broadcast"):
            run_broadcast_demo(spark)
        if args.demo in ("all", "window"):
            run_window_demo(spark)
        if args.demo in ("all", "union"):
            run_union_demo(spark)
    finally:
        stop_spark_session(spark)


if __name__ == "__main__":
    main()