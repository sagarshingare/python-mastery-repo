# PySpark Interview Questions, Architecture Tradeoffs & Coding Problems

> **Learning Path**: [Stage 06: Distributed Big Data](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-06-distributed-big-data) ▸ **Step 6.4: Spark Interview Prep & Lakehouse Tradeoffs**

A comprehensive collection of PySpark interview questions, Lakehouse architectural tradeoffs (Apache Iceberg, Delta Lake, Apache Hudi), file format comparisons, performance tuning, and LeetCode-style coding problems with detailed solutions.

---

## Coverage

### 1. Lakehouse & Ecosystem Tradeoffs (`Architecture_Tradeoffs`)
- **Open Table Formats: Apache Iceberg vs Delta Lake vs Apache Hudi**:
  - *Metadata Architecture*: Iceberg hierarchical snapshot tree (`metadata.json` -> manifest list -> manifest files -> data files) vs Delta linear transaction log (`_delta_log/*.json` + checkpoint Parquet) vs Hudi timeline service (`.hoodie/`).
  - *Hidden Partitioning*: Iceberg's query-transparent partition transforms (`days(ts)`, `bucket(16, id)`) and partition evolution without data rewrites vs Hive directory structures (`date=2024-01-01/`).
  - *Mutation & Concurrency*: Copy-on-Write (CoW) vs Merge-on-Read (MoR) with deletion vectors, positional deletes, and equality deletes.
  - *Multi-Engine Neutrality*: Iceberg's catalog-first design across Spark, Trino, Flink, DuckDB, Snowflake, BigQuery vs Delta's deep Databricks/Spark integration.
- **File Formats: Parquet vs ORC vs Avro**:
  - Parquet (columnar, Dremel nested shredding, dictionary/RLE encoding, predicate pushdown) for analytical queries.
  - ORC (Optimized Row Columnar with stripe-level indexes) for Hive/Trino.
  - Avro (row-oriented binary with JSON schema) for Kafka/streaming ingestion and low-latency writes.
- **Partition Management: Repartition vs Coalesce**:
  - Full network shuffle with balanced hash partitions vs local partition merging without shuffle (and the risk of partition skew).
- **Execution & Join Strategies**:
  - Broadcast Hash Join (BHJ) vs Shuffle Hash Join (SHJ) vs Sort-Merge Join (SMJ) vs Cartesian/BNL.
  - Data skew mitigation: Salting hot keys vs Spark 3+ Adaptive Query Execution (AQE).
- **Medallion Architecture Tradeoffs**:
  - Bronze (Raw landing, immutable audit) vs Silver (Cleansed, conformant, deduplicated) vs Gold (Aggregated business star-schemas). Storage volume vs pipeline latency vs replayability.

### 2. Fundamental Concepts (`PySpark_Fundamentals`)
- RDD vs DataFrame (abstraction levels, Catalyst optimization, 10-100x speedup)
- Catalyst Optimizer (Parsing -> Analyzing -> Logical Optimization -> Physical Planning -> Code Generation)
- Spark Shuffle (Exchange boundaries, network I/O, spills, and mitigation)
- Lazy Evaluation (DAG construction, optimization windows, execution triggers)

### 3. Partitioning & Memory Optimization (`Partitioning_Strategy`, `Memory_Management`)
- Optimal partition count calculation (`cores * 2 to 4`, ~128MB rule)
- Bucketing strategy and pre-sorted shuffle elimination
- Unified Memory Management (Storage vs Execution fraction, dynamic borrowing)
- Caching levels (`MEMORY_ONLY`, `MEMORY_AND_DISK_SER`, `OFF_HEAP`)

### 4. Most Asked Interview Questions (`Most_Asked_Questions`)
1. **Lazy Evaluation** - Why Spark postpones computation until action triggers
2. **DataFrame vs RDD** - When to drop to low-level RDD vs high-level DataFrame
3. **Memory Issues** - Diagnosing and resolving Driver OOM vs Executor OOM
4. **Skewed Data** - Identifying straggler tasks and applying salting / AQE
5. **Join Performance** - Choosing the optimal join strategy

### 5. Coding Problems (LeetCode Style) (`Coding_Problems`)
1. **Top N Salary** - Highest earners per department via window `row_number()`
2. **Duplicate Emails** - GroupBy and window counting filter
3. **Second Highest Salary** - Handling ties and NULLs with `dense_rank()`
4. **Cumulative Sum** - Running transactions balance with `rowsBetween`
5. **Top K Frequent** - GroupBy aggregation and sorting

### 6. Performance Tuning (`Performance_Tuning`)
- SQL vs DataFrame API execution equivalence
- Interpreting `df.explain(True)` physical plans, filters, and exchange nodes

---

## Interactive Command-Line Demos

Run all questions and tradeoffs, or focus on a specific module:

```bash
# Run all topics including Lakehouse tradeoffs
python3 -m pyspark.interview_questions.run_examples --demo all

# Run specific topic demonstrations
python3 -m pyspark.interview_questions.run_examples --demo tradeoffs
python3 -m pyspark.interview_questions.run_examples --demo fundamentals
python3 -m pyspark.interview_questions.run_examples --demo partitioning
python3 -m pyspark.interview_questions.run_examples --demo memory
python3 -m pyspark.interview_questions.run_examples --demo most_asked
python3 -m pyspark.interview_questions.run_examples --demo coding_problems
python3 -m pyspark.interview_questions.run_examples --demo performance
```