"""PySpark transformations module.

Exposes narrow and wide transformations, joins, broadcast optimizations,
and window analytical operations.
"""

from __future__ import annotations

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

__all__ = [
    "HAS_PYSPARK",
    "apply_map_transformation",
    "apply_window_analytics",
    "apply_window_function",
    "broadcast_join",
    "derive_columns",
    "filter_greater_than",
    "group_and_aggregate",
    "join_dataframes",
    "union_dataframes",
]