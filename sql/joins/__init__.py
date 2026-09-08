"""SQL Join patterns package: INNER, LEFT, ANTI-JOIN, SELF, CROSS, and FULL OUTER."""

from .join_operations import (
    create_connection,
    get_anti_join_departments,
    get_cross_join_combinations,
    get_full_outer_join_simulation,
    get_inner_join_records,
    get_left_join_records,
    get_self_join_hierarchy,
    init_joins_db,
)

__all__ = [
    "create_connection",
    "init_joins_db",
    "get_inner_join_records",
    "get_left_join_records",
    "get_anti_join_departments",
    "get_self_join_hierarchy",
    "get_cross_join_combinations",
    "get_full_outer_join_simulation",
]
