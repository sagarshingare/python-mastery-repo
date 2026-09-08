"""PySpark SQL module.

Exposes temporary/global views, CTE queries, window SQL, UDF registration,
and Spark Catalog inspection utilities.
"""

from __future__ import annotations

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

__all__ = [
    "HAS_PYSPARK",
    "create_global_temp_view",
    "create_temp_view",
    "execute_cte_query",
    "execute_sql_query",
    "execute_window_sql",
    "inspect_catalog",
    "register_python_udf",
    "register_vectorized_udf",
]
