"""SQL Query Optimization package: Execution plans, indexing, and sargability."""

from .query_optimizer import (
    benchmark_single_column_index,
    create_connection,
    demonstrate_composite_prefix_rule,
    demonstrate_sargability,
    explain_query_plan,
    init_optimization_db,
)

__all__ = [
    "create_connection",
    "init_optimization_db",
    "explain_query_plan",
    "benchmark_single_column_index",
    "demonstrate_composite_prefix_rule",
    "demonstrate_sargability",
]
