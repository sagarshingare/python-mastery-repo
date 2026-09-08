"""CLI runner for SQL Window Functions demonstrations."""

from __future__ import annotations

import argparse
import logging

from sql.window_functions.window_operations import (
    create_connection,
    get_month_over_month_growth,
    get_moving_aggregations,
    get_ranking_metrics,
    get_top_earners_per_dept,
    init_window_db,
)

logger = logging.getLogger(__name__)


def run_ranking_demo() -> None:
    logger.info("Running Window Functions: Ranking Metrics")
    conn = create_connection()
    try:
        init_window_db(conn)
        rows = get_ranking_metrics(conn)
        print("Department Ranking Functions (ROW_NUMBER vs RANK vs DENSE_RANK):")
        for r in rows:
            print(
                f"  [{r['department_name']}] {r['name'].ljust(18)} "
                f"${r['salary']:,.2f} | RowNum: {r['row_num']} | Rank: {r['rank_pos']} | DenseRank: {r['dense_rank_pos']}"
            )
    finally:
        conn.close()


def run_top_earners_demo() -> None:
    logger.info("Running Window Functions: Top-N Per Department")
    conn = create_connection()
    try:
        init_window_db(conn)
        top_earners = get_top_earners_per_dept(conn, top_n=2)
        print("Top 2 Highest Earners per Department (via DENSE_RANK):")
        for r in top_earners:
            print(f"  - [{r['department_name']}] Rank #{r['rank_in_dept']}: {r['name']} (${r['salary']:,.2f})")
    finally:
        conn.close()


def run_growth_demo() -> None:
    logger.info("Running Window Functions: LAG / LEAD MoM Growth")
    conn = create_connection()
    try:
        init_window_db(conn)
        growth = get_month_over_month_growth(conn)
        print("Time-Series Comparison (LAG & LEAD):")
        for r in growth:
            prior = f"${r['prior_month_revenue']:,.2f}" if r['prior_month_revenue'] is not None else "N/A"
            mom = f"{r['mom_growth_pct']:+.1f}%" if r['mom_growth_pct'] is not None else "0.0%"
            print(f"  - Month {r['sales_month']}: Rev=${r['revenue']:,.2f} | Prior={prior} | MoM={mom}")
    finally:
        conn.close()


def run_moving_demo() -> None:
    logger.info("Running Window Functions: Cumulative Sum and Moving Average")
    conn = create_connection()
    try:
        init_window_db(conn)
        moving = get_moving_aggregations(conn)
        print("Moving Window Frames (Cumulative & 3-Month Moving Average):")
        for r in moving:
            print(
                f"  - Month {r['sales_month']}: Rev=${r['revenue']:,.2f} | "
                f"Cumulative=${r['cumulative_revenue']:,.2f} | 3M Avg=${r['moving_avg_3m']:,.2f}"
            )
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="SQL Window Functions Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["ranking", "top_earners", "growth", "moving", "all"],
        default="all",
        help="Demonstration to run (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "ranking": run_ranking_demo,
        "top_earners": run_top_earners_demo,
        "growth": run_growth_demo,
        "moving": run_moving_demo,
    }

    if args.demo == "all":
        for fn in dispatch.values():
            fn()
            print()
    else:
        dispatch[args.demo]()


if __name__ == "__main__":
    main()
