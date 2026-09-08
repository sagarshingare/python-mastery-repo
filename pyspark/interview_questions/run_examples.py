"""Run PySpark interview questions and problems with CLI.

Interactive demonstration of interview questions, coding problems,
and most asked topics in PySpark interviews.
"""

from __future__ import annotations

import argparse
import json
import logging
from typing import Any, Dict

from pyspark.interview_questions.pyspark_interview import (
    Architecture_Tradeoffs,
    Coding_Problems,
    Memory_Management,
    Most_Asked_Questions,
    Partitioning_Strategy,
    Performance_Tuning,
    PySpark_Fundamentals,
)

logger = logging.getLogger(__name__)


def print_section(title: str, content: Dict[str, Any]) -> None:
    """Pretty print a section with title and content.
    
    Args:
        title: Section title.
        content: Dictionary content to display.
    """
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)
    
    for key, value in content.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  • {k}: {v}")
        elif isinstance(value, list):
            print(f"\n{key}:")
            for item in value:
                print(f"  • {item}")
        else:
            print(f"\n{key}:")
            print(f"  {value}")


def run_fundamentals() -> None:
    """Run fundamental concepts examples."""
    logger.info("Running Fundamentals examples")
    
    print("\n### FUNDAMENTAL CONCEPTS ###")
    
    # RDD vs DataFrame
    content = PySpark_Fundamentals.rdd_vs_dataframe()
    print_section("RDD vs DataFrame", content)
    
    # Catalyst Optimizer
    content = PySpark_Fundamentals.catalyst_optimizer()
    print_section("Catalyst Optimizer", content)
    
    # Shuffle
    content = PySpark_Fundamentals.shuffle_explain()
    print_section("Spark Shuffle Explained", content)


def run_partitioning() -> None:
    """Run partitioning strategy examples."""
    logger.info("Running Partitioning examples")
    
    print("\n### PARTITIONING & OPTIMIZATION ###")
    
    # Optimal partition count
    content = Partitioning_Strategy.optimal_partition_count()
    print_section("Optimal Partition Count", content)
    
    # Bucketing
    content = Partitioning_Strategy.bucketing_advantage()
    print_section("Bucketing Advantages", content)


def run_memory() -> None:
    """Run memory management examples."""
    logger.info("Running Memory Management examples")
    
    print("\n### MEMORY & CACHING ###")
    
    # Caching strategy
    content = Memory_Management.caching_strategy()
    print_section("Caching Strategy", content)
    
    # Broadcast vs Shuffle
    content = Memory_Management.broadcast_vs_shuffle()
    print_section("Broadcast vs Shuffle Join", content)


def run_most_asked() -> None:
    """Run most asked questions."""
    logger.info("Running Most Asked Questions")
    
    print("\n### MOST ASKED INTERVIEW QUESTIONS ###")
    
    questions = [
        ("Lazy Evaluation", Most_Asked_Questions.q1_what_is_lazy_evaluation()),
        ("DataFrame vs RDD", Most_Asked_Questions.q2_dataframe_vs_rdd()),
        ("Memory Issues", Most_Asked_Questions.q3_memory_issues()),
        ("Skewed Data", Most_Asked_Questions.q4_skewed_data()),
        ("Join Performance", Most_Asked_Questions.q5_join_performance()),
    ]
    
    for i, (title, content) in enumerate(questions, 1):
        print_section(f"Q{i}: {title}", content)


def run_coding_problems() -> None:
    """Run coding problems."""
    logger.info("Running Coding Problems")
    
    print("\n### CODING PROBLEMS ###")
    
    problems = [
        ("Top N Salary", Coding_Problems.problem_1_top_n_salary()),
        ("Duplicate Emails", Coding_Problems.problem_2_duplicate_emails()),
        ("Second Highest Salary", Coding_Problems.problem_3_second_highest_salary()),
        ("Cumulative Sum", Coding_Problems.problem_4_cumulative_sum()),
        ("Top K Frequent", Coding_Problems.problem_5_top_k_frequent()),
    ]
    
    for i, (title, content) in enumerate(problems, 1):
        print_section(f"Problem {i}: {title}", content)


def run_performance_tuning() -> None:
    """Run performance tuning examples."""
    logger.info("Running Performance Tuning examples")
    
    print("\n### PERFORMANCE TUNING ###")
    
    # SQL vs DataFrame
    content = Performance_Tuning.sql_vs_dataframe()
    print_section("SQL vs DataFrame API", content)
    
    # Explain plan
    content = Performance_Tuning.explain_plan()
    print_section("Reading Explain Plans", content)


def run_tradeoffs() -> None:
    """Run lakehouse and architectural tradeoffs examples."""
    logger.info("Running Architecture & Ecosystem Tradeoffs")
    
    print("\n### ARCHITECTURE & LAKEHOUSE TRADEOFFS (ICEBERG, DELTA, FILE FORMATS) ###")
    
    # 1. Open Table Formats
    content = Architecture_Tradeoffs.table_formats_iceberg_vs_delta_vs_hudi()
    print_section("Open Table Formats: Apache Iceberg vs Delta Lake vs Apache Hudi", content)
    
    # 2. File Formats
    content = Architecture_Tradeoffs.file_formats_parquet_vs_orc_vs_avro()
    print_section("File Serialization: Parquet vs ORC vs Avro", content)
    
    # 3. Repartition vs Coalesce
    content = Architecture_Tradeoffs.repartition_vs_coalesce()
    print_section("Partition Management: Repartition vs Coalesce", content)
    
    # 4. Join Strategies
    content = Architecture_Tradeoffs.join_strategies_tradeoffs()
    print_section("Execution Strategies: Join Selection & Skew Mitigation", content)
    
    # 5. Medallion Lakehouse Architecture
    content = Architecture_Tradeoffs.lakehouse_medallion_tradeoffs()
    print_section("Medallion Architecture: Bronze vs Silver vs Gold Tradeoffs", content)


def run_all() -> None:
    """Run all examples."""
    run_fundamentals()
    run_partitioning()
    run_memory()
    run_most_asked()
    run_coding_problems()
    run_performance_tuning()
    run_tradeoffs()


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="PySpark Interview Questions, Lakehouse Tradeoffs, and Coding Problems"
    )
    parser.add_argument(
        "--demo",
        "--module",
        dest="module",
        choices=[
            "fundamentals",
            "partitioning",
            "memory",
            "most_asked",
            "coding_problems",
            "performance",
            "tradeoffs",
            "all",
        ],
        default="all",
        help="Specific category or demonstration to run (default: all)",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "fundamentals":
        run_fundamentals()
    elif args.module == "partitioning":
        run_partitioning()
    elif args.module == "memory":
        run_memory()
    elif args.module == "most_asked":
        run_most_asked()
    elif args.module == "coding_problems":
        run_coding_problems()
    elif args.module == "performance":
        run_performance_tuning()
    elif args.module == "tradeoffs":
        run_tradeoffs()
    else:
        run_all()


if __name__ == "__main__":
    main()