"""CLI runner for Advanced SQL Patterns demonstrations."""

from __future__ import annotations

import argparse
import logging

from sql.advanced_queries.advanced_operations import (
    create_connection,
    detect_gaps_and_islands,
    get_user_preference,
    init_advanced_db,
    pivot_role_headcount,
    query_json_metadata,
    unpivot_quarterly_sales,
    upsert_user_preference,
)

logger = logging.getLogger(__name__)


def run_pivot_demo() -> None:
    logger.info("Running Advanced SQL: Conditional Aggregation Pivot")
    conn = create_connection()
    try:
        init_advanced_db(conn)
        rows = pivot_role_headcount(conn)
        print("Pivoted Role Counts per Department:")
        for r in rows:
            print(
                f"  [{r['department_name']}] Engineers: {r['engineers']}, "
                f"Managers: {r['managers']}, Designers: {r['designers']} (Total: {r['total_headcount']})"
            )
    finally:
        conn.close()


def run_unpivot_demo() -> None:
    logger.info("Running Advanced SQL: Unpivoting Columns to Rows")
    conn = create_connection()
    try:
        init_advanced_db(conn)
        rows = unpivot_quarterly_sales(conn)
        print("Unpivoted Sales Records (Wide to Long):")
        for r in rows:
            print(f"  - {r['product_id']} | {r['quarter']}: ${r['amount']:,.2f}")
    finally:
        conn.close()


def run_upsert_demo() -> None:
    logger.info("Running Advanced SQL: Atomic UPSERT (ON CONFLICT)")
    conn = create_connection()
    try:
        init_advanced_db(conn)
        pref_before = get_user_preference(conn, 42)
        print(f"Before UPSERT: {pref_before}")

        # Execute UPSERT updating theme and notification preference
        upsert_user_preference(
            conn,
            user_id=42,
            theme="solarized-light",
            notifications_enabled=False,
            updated_at="2026-06-15 14:30:00",
        )
        pref_after = get_user_preference(conn, 42)
        print(f"After UPSERT:  {pref_after}")

        # Insert brand new record via same UPSERT function
        upsert_user_preference(
            conn,
            user_id=99,
            theme="high-contrast",
            notifications_enabled=True,
            updated_at="2026-06-15 14:35:00",
        )
        pref_new = get_user_preference(conn, 99)
        print(f"New User UPSERT: {pref_new}")
    finally:
        conn.close()


def run_json_demo() -> None:
    logger.info("Running Advanced SQL: JSON Attribute Querying")
    conn = create_connection()
    try:
        init_advanced_db(conn)
        rows = query_json_metadata(conn)
        print("Semi-Structured JSON Query Results (json_extract):")
        for r in rows:
            print(
                f"  - {r['name'].ljust(18)} | Role: {r['role'].ljust(9)} | "
                f"Level: {r['seniority_level'].ljust(9)} | Loc: {r['location'].ljust(8)} | TopSkill: {r['primary_skill']}"
            )
    finally:
        conn.close()


def run_gaps_islands_demo() -> None:
    logger.info("Running Advanced SQL: Gaps & Islands Streak Analysis")
    conn = create_connection()
    try:
        init_advanced_db(conn)
        streaks = detect_gaps_and_islands(conn, min_streak_days=3)
        print("Detected Consecutive Daily Login Streaks (>= 3 days):")
        for s in streaks:
            print(
                f"  - User #{s['user_id']}: {s['consecutive_days']} consecutive days "
                f"({s['streak_start']} through {s['streak_end']})"
            )
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Advanced SQL Pattern Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["pivot", "unpivot", "upsert", "json", "gaps_islands", "all"],
        default="all",
        help="Demonstration to run (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "pivot": run_pivot_demo,
        "unpivot": run_unpivot_demo,
        "upsert": run_upsert_demo,
        "json": run_json_demo,
        "gaps_islands": run_gaps_islands_demo,
    }

    if args.demo == "all":
        for fn in dispatch.values():
            fn()
            print()
    else:
        dispatch[args.demo]()


if __name__ == "__main__":
    main()
