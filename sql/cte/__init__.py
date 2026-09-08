"""Common Table Expressions (CTEs) package: Modular non-recursive and recursive queries."""

from .cte_operations import (
    create_connection,
    generate_number_sequence,
    get_modular_pipeline_cte,
    get_org_chart_hierarchy,
    init_cte_db,
)

__all__ = [
    "create_connection",
    "init_cte_db",
    "get_modular_pipeline_cte",
    "generate_number_sequence",
    "get_org_chart_hierarchy",
]
