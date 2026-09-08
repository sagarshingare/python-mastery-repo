"""CLI runner for SQL Optimization and Indexing demonstrations."""

from __future__ import annotations

import argparse
import logging

from sql.optimization.query_optimizer import (
    benchmark_single_column_index,
    create_connection,
    demonstrate_composite_prefix_rule,
    demonstrate_sargability,
    explain_query_plan,
    init_optimization_db,
)

logger = logging.getLogger(__name__)


def run_explain_demo() -> None:
    logger.info("Running SQL Optimization: EXPLAIN QUERY PLAN inspection")
    conn = create_connection()
    try:
        init_optimization_db(conn)
        plan = explain_query_plan(conn, "SELECT COUNT(*) FROM orders WHERE total_amount > 300.0;")
        print("EXPLAIN QUERY PLAN Output:")
        for step in plan:
            print(f"  -> {step}")
    finally:
        conn.close()


def run_indexing_demo() -> None:
    logger.info("Running SQL Optimization: Single Column B-Tree Indexing")
    conn = create_connection()
    try:
        init_optimization_db(conn)
        res = benchmark_single_column_index(conn)
        print(f"Query: {res['query']}")
        print(f"  Before Index: {res['plan_before_index']}")
        print(f"  After Index:  {res['plan_after_index']}")
    finally:
        conn.close()


def run_composite_demo() -> None:
    logger.info("Running SQL Optimization: Composite Index Leftmost Prefix Rule")
    conn = create_connection()
    try:
        init_optimization_db(conn)
        comp = demonstrate_composite_prefix_rule(conn)
        print(f"Composite Index: {comp['composite_index']}\n")
        
        q_both = comp['query_prefix_and_second']
        print(f"Case 1 (Prefix + Second column): {q_both['query']}")
        print(f"  -> {q_both['plan']}\n")

        q_pref = comp['query_prefix_only']
        print(f"Case 2 (Prefix only): {q_pref['query']}")
        print(f"  -> {q_pref['plan']}\n")

        q_non = comp['query_non_prefix_only']
        print(f"Case 3 (Non-prefix column only): {q_non['query']}")
        print(f"  -> {q_non['plan']}")
    finally:
        conn.close()


def run_sargability_demo() -> None:
    logger.info("Running SQL Optimization: Sargability Refactoring")
    conn = create_connection()
    try:
        init_optimization_db(conn)
        sarg = demonstrate_sargability(conn)
        print("Non-Sargable (wrapping indexed column in function):")
        print(f"  Query: {sarg['non_sargable']['query']}")
        print(f"  Plan:  {sarg['non_sargable']['plan']}\n")

        print("Sargable (rewritten using direct range bounds):")
        print(f"  Query: {sarg['sargable']['query']}")
        print(f"  Plan:  {sarg['sargable']['plan']}")
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="SQL Query Optimization Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["explain", "indexing", "composite", "sargability", "all"],
        default="all",
        help="Demonstration to run (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "explain": run_explain_demo,
        "indexing": run_indexing_demo,
        "composite": run_composite_demo,
        "sargability": run_sargability_demo,
    }

    if args.demo == "all":
        for fn in dispatch.values():
            fn()
            print()
    else:
        dispatch[args.demo]()


if __name__ == "__main__":
    main()
