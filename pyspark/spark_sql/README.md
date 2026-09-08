# PySpark SQL & Views

> **Learning Path**: [Stage 06: Distributed Big Data](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-06-distributed-big-data) ▸ **Step 6.5: Spark SQL**

This module covers Apache Spark SQL, ANSI SQL dialect compliance, session-scoped and global temporary views, Common Table Expressions (WITH CTE), pure SQL window analytics, standard vs Vectorized Pandas UDFs, and the Spark Catalog API.

---

## Key Architecture & Concepts

1. **Temporary Views vs Global Views**:
   - `createOrReplaceTempView("tbl")`: Bound strictly to the current `SparkSession`. Discarded when the session terminates.
   - `createOrReplaceGlobalTempView("tbl")`: Cross-session view residing in the system-preserved `global_temp` database (`SELECT * FROM global_temp.tbl`).
2. **Common Table Expressions (WITH CTE)**:
   - Modular, readable SQL pipeline definitions optimized into the same Catalyst logical plan as raw subqueries.
3. **SQL Window Analytical Functions**:
   - `OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN ...)` for rankings, cumulative sums, and lag/lead lookups.
4. **Standard UDFs vs Vectorized Pandas UDFs**:
   - *Standard Python UDF*: Serializes individual row objects via Py4J into Python worker processes, incurring heavy serialization overhead.
   - *Vectorized Pandas UDF (`@pandas_udf`)*: Uses Apache Arrow for zero-copy in-memory column batching across JVM and Python workers, yielding 10x-100x speedups.
5. **Spark Catalog API**:
   - Programmatic metadata introspection (`spark.catalog.listDatabases()`, `listTables()`, `isCached()`).

---

## Files

| File | Description |
|------|-------------|
| `spark_sql.py` | Temp/global views, CTEs, SQL windowing, UDFs, and catalog inspection |
| `run_examples.py` | CLI demo runner with `--demo` selector |
| `examples.py` | Standard entry point alias |
| `__init__.py` | Public API exports |

---

## Interactive Demos

```bash
# Run all Spark SQL demonstrations
python3 -m pyspark.spark_sql.run_examples --demo all

# Run specific demonstrations
python3 -m pyspark.spark_sql.run_examples --demo views
python3 -m pyspark.spark_sql.run_examples --demo cte
python3 -m pyspark.spark_sql.run_examples --demo window
python3 -m pyspark.spark_sql.run_examples --demo udf
python3 -m pyspark.spark_sql.run_examples --demo catalog
```
