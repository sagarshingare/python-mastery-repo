"""Master CLI runner for Stage 06: Distributed Big Data (PySpark) suite."""

from __future__ import annotations

import argparse
import logging
import sys

from pyspark.basics.spark_basics import (
    HAS_PYSPARK,
    create_spark_session,
    stop_spark_session,
)
from pyspark.basics.run_examples import (
    run_create_dataframe_examples,
    run_create_spark_session_examples,
    run_filter_examples,
    run_inspect_dataframe_examples,
    run_select_examples,
)
from pyspark.transformations.run_examples import (
    create_employee_dataset,
    run_broadcast_demo,
    run_filter_demo,
    run_groupby_demo,
    run_join_demo,
    run_map_demo,
    run_union_demo,
    run_window_demo,
)
from pyspark.actions.run_examples import (
    create_sample_dataset as create_actions_dataset,
    run_collect_demo,
    run_count_demo,
    run_partition_demo,
    run_summary_demo,
    run_write_demo,
)
from pyspark.interview_questions.run_examples import (
    run_coding_problems,
    run_fundamentals,
    run_memory,
    run_most_asked,
    run_partitioning,
    run_performance_tuning,
    run_tradeoffs,
)

logger = logging.getLogger(__name__)


def run_all_basics(spark: object) -> None:
    print("================================================================================")
    print("              Step 6.1: Spark Basics & DataFrame Ingestion                      ")
    print("================================================================================")
    run_create_spark_session_examples(spark)
    run_create_dataframe_examples(spark)
    run_inspect_dataframe_examples(spark)
    run_filter_examples(spark)
    run_select_examples(spark)
    print()


def run_all_transformations(spark: object) -> None:
    print("================================================================================")
    print("        Step 6.2: Spark Transformations (Narrow/Wide, Broadcast & Window)       ")
    print("================================================================================")
    run_map_demo(spark)
    run_filter_demo(spark)
    run_groupby_demo(spark)
    run_join_demo(spark)
    run_broadcast_demo(spark)
    run_window_demo(spark)
    run_union_demo(spark)
    print()


def run_all_actions(spark: object) -> None:
    print("================================================================================")
    print("         Step 6.3: Spark Actions, Statistical Profiling & File Sinks            ")
    print("================================================================================")
    df = create_actions_dataset(spark)
    run_collect_demo(df)
    run_count_demo(df)
    run_summary_demo(df)
    run_write_demo(df)
    run_partition_demo(spark, df)
    print()


def run_all_interview_questions() -> None:
    print("================================================================================")
    print("        Step 6.4: Spark Architecture, Catalyst Optimizer & Interview Prep       ")
    print("================================================================================")
    run_fundamentals()
    run_partitioning()
    run_memory()
    run_most_asked()
    run_coding_problems()
    run_performance_tuning()
    run_tradeoffs()
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Master CLI for Stage 06: PySpark Distributed Big Data")
    parser.add_argument(
        "--submodule",
        choices=["basics", "transformations", "actions", "interview_questions", "all"],
        default="all",
        help="PySpark submodule to execute (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if not HAS_PYSPARK:
        print("❌ PySpark is not installed in the active environment.")
        sys.exit(1)

    spark = None
    needs_spark = args.submodule in ("all", "basics", "transformations", "actions")
    if needs_spark:
        spark = create_spark_session("PySpark-Master-Suite")

    try:
        if args.submodule in ("all", "basics"):
            run_all_basics(spark)
        if args.submodule in ("all", "transformations"):
            run_all_transformations(spark)
        if args.submodule in ("all", "actions"):
            run_all_actions(spark)
        if args.submodule in ("all", "interview_questions"):
            run_all_interview_questions()

        print("✅ All PySpark Stage 06 demonstrations executed successfully!")
    finally:
        if spark is not None:
            stop_spark_session(spark)


if __name__ == "__main__":
    main()
