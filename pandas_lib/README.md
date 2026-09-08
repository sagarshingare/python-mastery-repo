# Pandas Tabular Data Analytics

> **Learning Path**: [Stage 04: SQL](file:///Users/sagarshingare/Documents/python-mastery-repo/sql) ➔ [Stage 05: Data Analytics](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) ▸ **Step 5.2: Pandas Tabular Data**

Foundations and advanced patterns of tabular data processing in Python: Series, DataFrames, multi-column GroupBy aggregations, relational and time-series joins, rolling window smoothing, and high-performance memory optimization.

---

## Submodule Directory

| Submodule | Focus | Key Highlights |
|:---|:---|:---|
| [`basics/`](file:///Users/sagarshingare/Documents/python-mastery-repo/pandas_lib/basics) | Core Tabular Structures | Sales data cleaning, type coercion, missing value imputation, string parsing, datetime feature extraction |
| [`groupby/`](file:///Users/sagarshingare/Documents/python-mastery-repo/pandas_lib/groupby) | Split-Apply-Combine | Named aggregations (`.agg`), row-preserving transforms (`z-scores`), group filtering, multi-dimensional pivot tables |
| [`joins/`](file:///Users/sagarshingare/Documents/python-mastery-repo/pandas_lib/joins) | Merging & Alignment | Relational merges (inner, left, outer with indicator), index joins, concatenation, time-series `merge_asof` |
| [`window_functions/`](file:///Users/sagarshingare/Documents/python-mastery-repo/pandas_lib/window_functions) | Window Aggregation | Rolling mean/std, expanding cumulative metrics, exponential moving averages, partitioned ranking, period returns |
| [`optimization/`](file:///Users/sagarshingare/Documents/python-mastery-repo/pandas_lib/optimization) | Memory & Speed | Dtype downcasting (50-90% RAM reduction), categorical compression, chunked streaming, vectorization vs `apply()` |

---

## Running Demonstrations

### 1. Unified Master Demonstration
Execute all Pandas submodules sequentially:
```bash
python3 -m pandas_lib.run_examples --submodule all
# or
python3 -m pandas_lib.examples
```

### 2. Direct Submodule Runners
```bash
# Dataframe ingestion, cleaning, and features
python3 -m pandas_lib.basics.run_examples --demo all

# GroupBy aggregations, transformations, and pivots
python3 -m pandas_lib.groupby.run_examples --demo all

# Relational merges, joins, and asof time series alignment
python3 -m pandas_lib.joins.run_examples --demo all

# Rolling metrics, expanding windows, and partitioned ranking
python3 -m pandas_lib.window_functions.run_examples --demo all

# Memory downcasting, chunking, and apply vs vectorization benchmarks
python3 -m pandas_lib.optimization.run_examples --demo all
```
