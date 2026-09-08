# Stage 06: Distributed Big Data (PySpark)

> **Learning Path**: [Stage 06: Distributed Big Data](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-06-distributed-big-data) (Prerequisites: [Stage 01: Core Python](file:///Users/sagarshingare/Documents/python-mastery-repo/core_python), [Stage 04: SQL Mastery](file:///Users/sagarshingare/Documents/python-mastery-repo/sql), [Stage 05: Data Analytics](file:///Users/sagarshingare/Documents/python-mastery-repo/pandas_lib))

A production-grade collection of Apache Spark and PySpark engineering modules covering session orchestration, DataFrame operations, narrow vs wide transformations, broadcast joins, window analytics, distributed file persistence (Parquet, CSV, JSON), partition pruning, and Catalyst query optimization.

---

## Curriculum Steps

| Step | Submodule | Key Capabilities |
|:-----|:----------|:-----------------|
| **Step 6.1** | [`basics/`](file:///Users/sagarshingare/Documents/python-mastery-repo/pyspark/basics) | SparkSession lifecycle (`master("local[1]")`, resource safety), `StructType` schema definitions, DataFrame ingestion from lists & dicts, metadata inspection, and column filtering. |
| **Step 6.2** | [`transformations/`](file:///Users/sagarshingare/Documents/python-mastery-repo/pyspark/transformations) | Narrow transformations (in-memory map, filter, column derivation) vs wide transformations (groupBy, shuffle joins), Broadcast Hash Joins (`broadcast(small_df)`), and window analytical functions (`row_number()`, `dense_rank()`, cumulative sums). |
| **Step 6.3** | [`actions/`](file:///Users/sagarshingare/Documents/python-mastery-repo/pyspark/actions) | Action evaluation DAG triggers (`collect()`, `count()`, `take()`, `first()`), driver memory management, statistical profiling (`summary()`), multi-format persistence (Parquet, CSV, JSON), and partitioned directory sinks (`partitionBy()`). |
| **Step 6.4** | [`interview_questions/`](file:///Users/sagarshingare/Documents/python-mastery-repo/pyspark/interview_questions) | Catalyst optimizer pipeline (Parsed -> Analyzed -> Optimized -> Physical Plan), shuffle internals, partition tuning, memory storage vs execution pools, Lakehouse table formats (Apache Iceberg vs Delta Lake vs Apache Hudi, hidden partitioning, CoW vs MoR), storage formats (Parquet vs ORC vs Avro), and 5 LeetCode-style Spark coding problems. |

---

## Quick Start

```python
from pyspark.basics.spark_basics import create_spark_session, create_dataframe_from_list, sample_data, define_custom_schema
from pyspark.transformations.transformations import broadcast_join, apply_window_function
from pyspark.actions.actions import write_partitioned, summarize_dataframe, stop_spark_session

# 1. Initialize local SparkSession
spark = create_spark_session("QuickStartApp")

try:
    # 2. Ingest DataFrame with explicit schema
    schema = define_custom_schema()
    df = create_dataframe_from_list(spark, sample_data(), schema=schema)
    df.show()

    # 3. Apply window ranking
    ranked_df = apply_window_function(df, partition_col="department", order_col="salary")
    ranked_df.show()

    # 4. Generate statistical summary
    summary_df = summarize_dataframe(df)
    summary_df.show()
finally:
    stop_spark_session(spark)
```

---

## Interactive Command-Line Demonstrations

### Master Runner (All Submodules)

Run all submodules sequentially through the unified entry point:

```bash
# Run all Stage 06 demonstrations
python3 -m pyspark.run_examples --submodule all

# Or run via the entry point alias
python3 -m pyspark.examples --submodule all
```

### Individual Submodules

```bash
# Step 6.1: Spark Basics
python3 -m pyspark.basics.run_examples --demo all

# Step 6.2: Spark Transformations
python3 -m pyspark.transformations.run_examples --demo all

# Step 6.3: Spark Actions & Sinks
python3 -m pyspark.actions.run_examples --demo all

# Step 6.4: Spark Interview Prep & Optimization
python3 -m pyspark.interview_questions.run_examples --demo all
```

---

## Automated Verification

Execute the comprehensive PySpark test suite:

```bash
python3 -m pytest testing/pytest/test_pyspark_suite.py -v
```
