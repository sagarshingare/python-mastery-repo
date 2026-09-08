# PySpark Transformations

> **Learning Path**: [Stage 06: Distributed Big Data](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-06-distributed-big-data) ▸ **Step 6.2: Spark Transformations**

This module demonstrates PySpark transformations, contrasting narrow operations (in-memory, pipelineable without shuffling) with wide operations (requiring cluster-wide stage boundaries and shuffles), alongside broadcast joins and window analytics.

---

## Key Concepts & Architecture

1. **Narrow Transformations (No Shuffle)**:
   - Evaluated within the local partition executor without data movement across the network.
   - Operations: `filter()`, `select()`, `withColumn()`, conditional expressions (`when().otherwise()`).
2. **Wide Transformations (Shuffle Boundaries)**:
   - Data with the same key across partitions must be regrouped over the network into new partitions.
   - Operations: `groupBy().agg()`, standard `join()`, `distinct()`.
3. **Broadcast Hash Joins**:
   - For small lookup/dimension tables (default threshold 10MB in Spark), broadcasts copies to all executors.
   - Eliminates shuffle of the large fact table completely.
4. **Window Analytical Functions**:
   - `Window.partitionBy().orderBy()` for partitions without collapsing rows.
   - Ranking (`row_number()`, `dense_rank()`) and cumulative aggregates (`running_total`).

---

## Files

| File | Description |
|------|-------------|
| `transformations.py` | Implementation of narrow/wide transformations, broadcast joins, and window analytics |
| `run_examples.py` | CLI demo runner with `--demo` selector |
| `examples.py` | Standard entry point alias |
| `__init__.py` | Public API exports for `pyspark.transformations` |

---

## Interactive Demos

Run all demonstrations or select a specific transformation category:

```bash
# Run all transformation demonstrations
python3 -m pyspark.transformations.run_examples --demo all

# Run specific transformation categories
python3 -m pyspark.transformations.run_examples --demo map
python3 -m pyspark.transformations.run_examples --demo filter
python3 -m pyspark.transformations.run_examples --demo groupby
python3 -m pyspark.transformations.run_examples --demo join
python3 -m pyspark.transformations.run_examples --demo broadcast
python3 -m pyspark.transformations.run_examples --demo window
python3 -m pyspark.transformations.run_examples --demo union
```

Or execute via the `examples.py` entry point:

```bash
python3 -m pyspark.transformations.examples --demo all
```