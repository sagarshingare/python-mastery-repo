# PySpark Basics

> **Learning Path**: [Stage 06: Distributed Big Data](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-06-distributed-big-data) ▸ **Step 6.1: Spark Basics**

This module contains foundational Apache Spark and PySpark examples, covering session creation, DataFrame ingestion, schema definitions, and DataFrame inspection.

---

## Key Concepts & Implementation

- **SparkSession Lifecycle**: Creating isolated local sessions (`master("local[1]")`, disabling UI to minimize resource overhead) and stopping contexts cleanly.
- **Custom Schema Definition**: Building `StructType` and `StructField` instances with native PySpark types (`IntegerType`, `StringType`, `DoubleType`).
- **DataFrame Ingestion**: Creating DataFrames from Python lists of tuples and dictionaries.
- **Metadata Inspection**: Schema printing, `.dtypes`, `.columns`, row counts, and sample display.
- **Projections & Filtering**: Column selection and row filtering with SQL expressions and column predicates.

---

## Files

| File | Description |
|------|-------------|
| `spark_basics.py` | SparkSession lifecycle, schemas, DataFrame creation, and basic filtering |
| `run_examples.py` | Command-line demo runner with `--demo` selector |
| `examples.py` | Standard entry point alias for CLI execution |
| `__init__.py` | Public API exports for `pyspark.basics` |

---

## Interactive Demos

Run all demonstrations or focus on a specific concept:

```bash
# Run all basic Spark demonstrations
python3 -m pyspark.basics.run_examples --demo all

# Run specific demonstrations
python3 -m pyspark.basics.run_examples --demo session
python3 -m pyspark.basics.run_examples --demo dataframe
python3 -m pyspark.basics.run_examples --demo inspect
python3 -m pyspark.basics.run_examples --demo filter
python3 -m pyspark.basics.run_examples --demo select
```

Or execute via the `examples.py` entry point:

```bash
python3 -m pyspark.basics.examples --demo all
```