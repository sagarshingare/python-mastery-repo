"""Unified SQL Master Demonstration Runner.

Executes real SQL queries across in-memory SQLite instances covering fundamentals,
relational joins, Common Table Expressions, analytical window functions,
query plan optimization/indexing, and advanced patterns.
"""

from __future__ import annotations

import argparse
import logging

from sql.advanced_queries.run_examples import (
    run_gaps_islands_demo,
    run_json_demo,
    run_pivot_demo,
    run_unpivot_demo,
    run_upsert_demo,
)
from sql.basics.run_examples import (
    run_aggregation_demo,
    run_crud_demo,
    run_filtering_demo,
    run_pagination_demo,
)
from sql.cte.run_examples import (
    run_hierarchy_demo,
    run_modular_demo,
    run_sequence_demo,
)
from sql.joins.run_examples import (
    run_anti_demo,
    run_cross_demo,
    run_full_demo,
    run_inner_demo,
    run_left_demo,
    run_self_demo,
)
from sql.optimization.run_examples import (
    run_composite_demo,
    run_explain_demo,
    run_indexing_demo,
    run_sargability_demo,
)
from sql.window_functions.run_examples import (
    run_growth_demo,
    run_moving_demo,
    run_ranking_demo,
    run_top_earners_demo,
)

logger = logging.getLogger(__name__)


def run_all_basics() -> None:
    print("================================================================================")
    print("                         Step 4.1: SQL Fundamentals                             ")
    print("================================================================================")
    run_crud_demo()
    print()
    run_filtering_demo()
    print()
    run_aggregation_demo()
    print()
    run_pagination_demo()
    print()


def run_all_joins() -> None:
    print("================================================================================")
    print("                         Step 4.2: SQL Join Patterns                            ")
    print("================================================================================")
    run_inner_demo()
    print()
    run_left_demo()
    print()
    run_anti_demo()
    print()
    run_self_demo()
    print()
    run_cross_demo()
    print()
    run_full_demo()
    print()


def run_all_cte() -> None:
    print("================================================================================")
    print("                   Step 4.3: Common Table Expressions (CTEs)                    ")
    print("================================================================================")
    run_modular_demo()
    print()
    run_sequence_demo()
    print()
    run_hierarchy_demo()
    print()


def run_all_window() -> None:
    print("================================================================================")
    print("                       Step 4.4: SQL Window Functions                           ")
    print("================================================================================")
    run_ranking_demo()
    print()
    run_top_earners_demo()
    print()
    run_growth_demo()
    print()
    run_moving_demo()
    print()


def run_all_advanced() -> None:
    print("================================================================================")
    print("                       Step 4.5: Advanced SQL Patterns                          ")
    print("================================================================================")
    run_pivot_demo()
    print()
    run_unpivot_demo()
    print()
    run_upsert_demo()
    print()
    run_json_demo()
    print()
    run_gaps_islands_demo()
    print()


def run_all_optimization() -> None:
    print("================================================================================")
    print("                 Step 4.6: Query Optimization & Plan Analysis                   ")
    print("================================================================================")
    run_explain_demo()
    print()
    run_indexing_demo()
    print()
    run_composite_demo()
    print()
    run_sargability_demo()
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Unified SQL Mastery Suite Runner")
    parser.add_argument(
        "--submodule",
        choices=["basics", "joins", "cte", "window", "advanced", "optimization", "all"],
        default="all",
        help="Submodule to execute (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "basics": run_all_basics,
        "joins": run_all_joins,
        "cte": run_all_cte,
        "window": run_all_window,
        "advanced": run_all_advanced,
        "optimization": run_all_optimization,
    }

    if args.submodule == "all":
        for fn in dispatch.values():
            fn()
        print("✅ All SQL demonstrations executed successfully across all submodules!")
    else:
        dispatch[args.submodule]()


if __name__ == "__main__":
    main()
