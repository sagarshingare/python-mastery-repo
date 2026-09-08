"""SQL Window Functions package: Ranking, Lead/Lag comparisons, and moving frames."""

from .window_operations import (
    create_connection,
    get_month_over_month_growth,
    get_moving_aggregations,
    get_ranking_metrics,
    get_top_earners_per_dept,
    init_window_db,
)

__all__ = [
    "create_connection",
    "init_window_db",
    "get_ranking_metrics",
    "get_top_earners_per_dept",
    "get_month_over_month_growth",
    "get_moving_aggregations",
]
