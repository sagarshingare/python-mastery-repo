"""PySpark SQL - Temporary views, CTEs, window functions, UDFs, and Catalog API.

This module demonstrates Spark SQL capabilities:
- Session-scoped temporary views (`createOrReplaceTempView`)
- Global cross-session temporary views (`createOrReplaceGlobalTempView` in `global_temp`)
- Complex SQL analytics: CTEs (Common Table Expressions) and SQL Window Functions
- Standard Python User-Defined Functions (UDFs) and Arrow-optimized Vectorized Pandas UDFs
- Metadata exploration using the `spark.catalog` API

Python version: 3.9+
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

try:
    from pyspark.sql import DataFrame, SparkSession
    from pyspark.sql.functions import col, pandas_udf, udf
    from pyspark.sql.types import DoubleType, IntegerType, StringType
    HAS_PYSPARK = True
except ImportError:  # pragma: no cover
    HAS_PYSPARK = False
    DataFrame = Any  # type: ignore[misc, assignment]
    SparkSession = Any  # type: ignore[misc, assignment]

logger = logging.getLogger(__name__)


def create_temp_view(df: Optional[DataFrame], view_name: str) -> bool:
    """Register a DataFrame as a session-scoped temporary SQL view.

    Args:
        df: Source DataFrame.
        view_name: Name of the SQL table view.

    Returns:
        True if registration succeeded, False otherwise.
    """
    if df is None or not HAS_PYSPARK:
        return False

    try:
        df.createOrReplaceTempView(view_name)
        return True
    except Exception as exc:
        logger.error("Error creating temp view %s: %s", view_name, exc)
        return False


def create_global_temp_view(df: Optional[DataFrame], view_name: str) -> bool:
    """Register a DataFrame as a global cross-session temporary view.

    Global views reside in the system `global_temp` database.

    Args:
        df: Source DataFrame.
        view_name: View name.

    Returns:
        True if registration succeeded, False otherwise.
    """
    if df is None or not HAS_PYSPARK:
        return False

    try:
        df.createOrReplaceGlobalTempView(view_name)
        return True
    except Exception as exc:
        logger.error("Error creating global temp view %s: %s", view_name, exc)
        return False


def execute_sql_query(spark: Optional[SparkSession], query: str) -> Optional[DataFrame]:
    """Execute a raw SQL query against registered views and tables.

    Args:
        spark: Active SparkSession.
        query: SQL string to execute.

    Returns:
        Resulting DataFrame or None on error.
    """
    if spark is None or not HAS_PYSPARK:
        return None

    try:
        return spark.sql(query)
    except Exception as exc:
        logger.error("Error executing SQL query [%s]: %s", query, exc)
        return None


def execute_cte_query(spark: Optional[SparkSession], source_view: str = "employees") -> Optional[DataFrame]:
    """Execute a multi-stage Common Table Expression (WITH CTE) in Spark SQL.

    Computes department summary metrics and flags departments paying above company average.

    Args:
        spark: Active SparkSession.
        source_view: View name containing employee data.

    Returns:
        Resulting DataFrame with CTE calculations.
    """
    query = f"""
    WITH DeptStats AS (
        SELECT 
            dept,
            COUNT(*) as emp_count,
            AVG(salary) as avg_salary,
            MAX(salary) as max_salary
        FROM {source_view}
        GROUP BY dept
    ),
    CompanyStats AS (
        SELECT AVG(salary) as company_avg_salary FROM {source_view}
    )
    SELECT 
        d.dept,
        d.emp_count,
        ROUND(d.avg_salary, 2) as avg_salary,
        d.max_salary,
        CASE 
            WHEN d.avg_salary > c.company_avg_salary THEN 'Above Average'
            ELSE 'At/Below Average'
        END as benchmark
    FROM DeptStats d
    CROSS JOIN CompanyStats c
    ORDER BY d.avg_salary DESC
    """
    return execute_sql_query(spark, query)


def execute_window_sql(spark: Optional[SparkSession], source_view: str = "employees") -> Optional[DataFrame]:
    """Execute SQL analytical window functions (DENSE_RANK, SUM OVER, LAG).

    Args:
        spark: Active SparkSession.
        source_view: View name containing employee data.

    Returns:
        Resulting DataFrame with window metrics.
    """
    query = f"""
    SELECT 
        id,
        name,
        dept,
        salary,
        DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) as dept_rank,
        ROUND(SUM(salary) OVER (PARTITION BY dept ORDER BY salary DESC 
              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) as running_dept_salary,
        LAG(salary, 1, 0.0) OVER (PARTITION BY dept ORDER BY salary DESC) as next_higher_salary
    FROM {source_view}
    ORDER BY dept, dept_rank
    """
    return execute_sql_query(spark, query)


def register_python_udf(
    spark: Optional[SparkSession],
    func: Any,
    udf_name: str,
    return_type: Any = StringType(),
) -> bool:
    """Register a standard Python function as a Spark SQL UDF.

    Args:
        spark: Active SparkSession.
        func: Python callable.
        udf_name: Name used to invoke the UDF in SQL statements.
        return_type: PySpark DataType (e.g. StringType(), DoubleType()).

    Returns:
        True if registration succeeded, False otherwise.
    """
    if spark is None or not HAS_PYSPARK:
        return False

    try:
        spark.udf.register(udf_name, func, return_type)
        return True
    except Exception as exc:
        logger.error("Error registering Python UDF %s: %s", udf_name, exc)
        return False


def register_vectorized_udf(
    spark: Optional[SparkSession],
    udf_name: str = "vectorized_tax",
) -> bool:
    """Register an Apache Arrow Vectorized Pandas UDF for high-throughput numeric batching.

    Args:
        spark: Active SparkSession.
        udf_name: UDF name in SQL.

    Returns:
        True if registration succeeded, False otherwise.
    """
    if spark is None or not HAS_PYSPARK:
        return False

    try:
        import pandas as pd

        @pandas_udf("double")
        def compute_tax(salary_series: Any) -> Any:
            """Vectorized tax calculation executing across pandas series."""
            return salary_series * 0.22

        spark.udf.register(udf_name, compute_tax)
        return True
    except Exception as exc:
        logger.warning("Vectorized Pandas UDF unavailable (pyarrow/pandas issue): %s", exc)
        # Fallback to standard Python UDF
        def compute_tax_scalar(s: float) -> float:
            return round(s * 0.22, 2) if s is not None else 0.0

        spark.udf.register(udf_name, compute_tax_scalar, DoubleType())
        return True


def inspect_catalog(spark: Optional[SparkSession]) -> Dict[str, Any]:
    """Inspect Spark's in-memory and metastore catalog.

    Args:
        spark: Active SparkSession.

    Returns:
        Dictionary detailing databases, registered tables, and cached views.
    """
    if spark is None or not HAS_PYSPARK:
        return {}

    try:
        databases = [db.name for db in spark.catalog.listDatabases()]
        tables = [t.name for t in spark.catalog.listTables()]
        return {
            "current_database": spark.catalog.currentDatabase(),
            "databases": databases,
            "tables": tables,
            "is_cached": {t: spark.catalog.isCached(t) for t in tables},
        }
    except Exception as exc:
        logger.error("Error inspecting Spark catalog: %s", exc)
        return {}
