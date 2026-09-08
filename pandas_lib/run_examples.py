"""Master CLI runner for Pandas mastery suite."""

from __future__ import annotations

import argparse
import logging

from pandas_lib.basics.run_examples import (
    run_cleaning_demo,
    run_datetime_demo,
    run_missing_data_demo,
)
from pandas_lib.groupby.run_examples import (
    demo_filtering,
    demo_named_aggregation,
    demo_pivot,
    demo_transformations,
)
from pandas_lib.joins.run_examples import (
    demo_asof_merge,
    demo_concatenation,
    demo_index_joins,
    demo_relational_merges,
)
from pandas_lib.optimization.run_examples import (
    demo_chunking,
    demo_memory_downcasting,
    demo_vectorization_benchmark,
)
from pandas_lib.window_functions.run_examples import (
    demo_ema,
    demo_expanding,
    demo_lag_lead,
    demo_ranking,
    demo_rolling,
)

logger = logging.getLogger(__name__)


def run_all_basics() -> None:
    print("================================================================================")
    print("                 Pandas: Basics, Cleaning & Feature Engineering                 ")
    print("================================================================================")
    run_cleaning_demo()
    print()
    run_missing_data_demo()
    print()
    run_datetime_demo()
    print()


def run_all_groupby() -> None:
    print("================================================================================")
    print("                Pandas: GroupBy Aggregations, Transforms & Pivots               ")
    print("================================================================================")
    demo_named_aggregation()
    demo_transformations()
    demo_filtering()
    demo_pivot()
    print()


def run_all_joins() -> None:
    print("================================================================================")
    print("                Pandas: Relational Merges, Joins & Asof Alignment                ")
    print("================================================================================")
    demo_relational_merges()
    demo_index_joins()
    demo_concatenation()
    demo_asof_merge()
    print()


def run_all_window() -> None:
    print("================================================================================")
    print("             Pandas: Rolling, Expanding, Ranking & Lag/Lead Return              ")
    print("================================================================================")
    demo_rolling()
    demo_expanding()
    demo_ema()
    demo_ranking()
    demo_lag_lead()
    print()


def run_all_optimization() -> None:
    print("================================================================================")
    print("            Pandas: Memory Downcasting, Chunking & SIMD Vectorization           ")
    print("================================================================================")
    demo_memory_downcasting()
    demo_chunking()
    demo_vectorization_benchmark()
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Pandas Master Suite Demonstrations")
    parser.add_argument(
        "--submodule",
        choices=["basics", "groupby", "joins", "window_functions", "optimization", "all"],
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
        "groupby": run_all_groupby,
        "joins": run_all_joins,
        "window_functions": run_all_window,
        "optimization": run_all_optimization,
    }

    if args.submodule == "all":
        for fn in dispatch.values():
            fn()
        print("✅ All Pandas demonstrations executed successfully across all submodules!")
    else:
        dispatch[args.submodule]()


if __name__ == "__main__":
    main()
