"""Run PySpark SQL demonstrations with a comprehensive CLI."""

from __future__ import annotations

import argparse
import logging
from typing import Optional

from pyspark.basics.spark_basics import (
    create_spark_session,
    stop_spark_session,
)
from pyspark.spark_sql.spark_sql import (
    HAS_PYSPARK,
    create_global_temp_view,
    create_temp_view,
    execute_cte_query,
    execute_sql_query,
    execute_window_sql,
    inspect_catalog,
    register_python_udf,
    register_vectorized_udf,
)

logger = logging.getLogger(__name__)


def create_sample_sql_df(spark: object) -> object:
    """Create sample records for SQL demonstrations."""
    data = [
        (1, "Alice", "Engineering", 95000.0),
        (2, "Bob", "Marketing", 62000.0),
        (3, "Charlie", "Engineering", 110000.0),
        (4, "Diana", "Product", 88000.0),
        (5, "Evan", "Engineering", 105000.0),
        (6, "Fiona", "Marketing", 75000.0),
    ]
    return spark.createDataFrame(data, ["id", "name", "dept", "salary"])


def run_views_demo(spark: object) -> None:
    print("\n--- 1. Temporary & Global SQL Views ---")
    df = create_sample_sql_df(spark)
    create_temp_view(df, "employees")
    create_global_temp_view(df, "global_employees")

    print("Session-Scoped View (`employees`):")
    res1 = execute_sql_query(spark, "SELECT name, dept, salary FROM employees WHERE salary >= 90000")
    if res1:
        res1.show()

    print("Cross-Session Global View (`global_temp.global_employees`):")
    res2 = execute_sql_query(spark, "SELECT COUNT(*) as total_employees FROM global_temp.global_employees")
    if res2:
        res2.show()


def run_cte_demo(spark: object) -> None:
    print("\n--- 2. Common Table Expressions (WITH CTE) in Spark SQL ---")
    df = create_sample_sql_df(spark)
    create_temp_view(df, "employees")

    cte_df = execute_cte_query(spark, source_view="employees")
    if cte_df:
        print("Department Benchmark Summary (via CTE & Cross Join):")
        cte_df.show()


def run_window_demo(spark: object) -> None:
    print("\n--- 3. Pure SQL Window Analytics (DENSE_RANK & Running Total) ---")
    df = create_sample_sql_df(spark)
    create_temp_view(df, "employees")

    window_df = execute_window_sql(spark, source_view="employees")
    if window_df:
        print("Department Window Metrics:")
        window_df.show()


def run_udf_demo(spark: object) -> None:
    print("\n--- 4. User-Defined Functions (Standard vs Vectorized Pandas UDF) ---")
    df = create_sample_sql_df(spark)
    create_temp_view(df, "employees")

    # 1. Standard Python UDF
    def format_title(name: str, dept: str) -> str:
        return f"{name} [{dept.upper()}]"

    register_python_udf(spark, format_title, "format_badge")

    # 2. Vectorized Arrow / Pandas UDF
    register_vectorized_udf(spark, "estimate_tax")

    query = """
    SELECT 
        name,
        dept,
        salary,
        format_badge(name, dept) as employee_badge,
        ROUND(estimate_tax(salary), 2) as estimated_annual_tax
    FROM employees
    LIMIT 5
    """
    res = execute_sql_query(spark, query)
    if res:
        print("UDF & Vectorized Arrow Computation Output:")
        res.show(truncate=False)


def run_catalog_demo(spark: object) -> None:
    print("\n--- 5. Spark Metastore & In-Memory Catalog Inspection ---")
    df = create_sample_sql_df(spark)
    create_temp_view(df, "employees")

    catalog_meta = inspect_catalog(spark)
    print(f"Current Database: {catalog_meta.get('current_database')}")
    print(f"Databases:        {catalog_meta.get('databases')}")
    print(f"Registered Views: {catalog_meta.get('tables')}")
    print(f"Cache Status:     {catalog_meta.get('is_cached')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PySpark SQL Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["views", "cte", "window", "udf", "catalog", "all"],
        default="all",
        help="Demonstration to execute (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if not HAS_PYSPARK:
        print("PySpark is not installed. Skipping demo.")
        return

    spark = create_spark_session("Spark-SQL-Demo")
    try:
        if args.demo in ("all", "views"):
            run_views_demo(spark)
        if args.demo in ("all", "cte"):
            run_cte_demo(spark)
        if args.demo in ("all", "window"):
            run_window_demo(spark)
        if args.demo in ("all", "udf"):
            run_udf_demo(spark)
        if args.demo in ("all", "catalog"):
            run_catalog_demo(spark)
    finally:
        stop_spark_session(spark)


if __name__ == "__main__":
    main()
