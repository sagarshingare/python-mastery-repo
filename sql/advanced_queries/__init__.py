"""Advanced SQL Patterns package: Conditional pivot, unpivoting, UPSERT, JSON, and Gaps & Islands."""

from .advanced_operations import (
    create_connection,
    detect_gaps_and_islands,
    get_user_preference,
    init_advanced_db,
    pivot_role_headcount,
    query_json_metadata,
    unpivot_quarterly_sales,
    upsert_user_preference,
)

__all__ = [
    "create_connection",
    "init_advanced_db",
    "pivot_role_headcount",
    "unpivot_quarterly_sales",
    "upsert_user_preference",
    "get_user_preference",
    "query_json_metadata",
    "detect_gaps_and_islands",
]
