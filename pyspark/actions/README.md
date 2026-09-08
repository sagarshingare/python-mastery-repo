# PySpark Actions & Sinks

> **Learning Path**: [Stage 06: Distributed Big Data](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-06-distributed-big-data) ▸ **Step 6.3: Spark Actions & Sinks**

This module demonstrates PySpark actions that trigger execution DAGs, data retrieval to the driver process, statistical summarization, and distributed storage persistence across multiple file formats (Parquet, CSV, JSON) and partitioned directory layouts.

---

## Key Concepts & Architecture

1. **Actions vs Transformations**:
   - Transformations build an execution DAG lazily; actions evaluate the DAG and submit Spark jobs to executors.
   - Operations: `.collect()`, `.count()`, `.take()`, `.first()`, `.show()`.
2. **Driver Memory Management**:
   - Avoid calling `.collect()` on large datasets because all rows across all executor partitions are transmitted over the network into the single driver process JVM, risking Out-Of-Memory (OOM) crashes.
   - Use `.take(n)` or `.head(n)` for inspecting samples safely.
3. **Statistical Profiling**:
   - `.summary()` executes distributed count, mean, stddev, min, and quartile calculations in parallel without moving raw data to the driver.
4. **Columnar & Partitioned File Sinks**:
   - Columnar Parquet format with Snappy compression for maximum compression ratios and predicate pushdown.
   - Partitioning by dimension columns (e.g., `partitionBy("dept")`) creates folder structures that Spark's Catalyst optimizer leverages for partition pruning during queries.

---

## Files

| File | Description |
|------|-------------|
| `actions.py` | Eager actions, statistical profiling, and multi-format file writer/reader utilities |
| `run_examples.py` | CLI demo runner with `--demo` selector |
| `examples.py` | Standard entry point alias |
| `__init__.py` | Public API exports for `pyspark.actions` |

---

## Interactive Demos

Run all demonstrations or focus on a specific action topic:

```bash
# Run all action and persistence demonstrations
python3 -m pyspark.actions.run_examples --demo all

# Run specific demonstrations
python3 -m pyspark.actions.run_examples --demo collect
python3 -m pyspark.actions.run_examples --demo count
python3 -m pyspark.actions.run_examples --demo summary
python3 -m pyspark.actions.run_examples --demo write
python3 -m pyspark.actions.run_examples --demo partition
```

Or execute via the `examples.py` entry point:

```bash
python3 -m pyspark.actions.examples --demo all
```