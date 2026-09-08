# Pandas Relational Joins & Merges

> **Learning Path**: [Stage 05: Data Analytics & Scientific Libraries](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) — **Step 5.2**

Combining and aligning datasets: relational joins (`pd.merge`), index alignment (`DataFrame.join`), vertical/horizontal stacking (`pd.concat`), and approximate temporal matching (`pd.merge_asof`).

---

## Key Operations

1. **Relational Merges (`pd.merge`)**: Inner, left, right, and outer joins with `indicator=True` to track source origins (`both`, `left_only`, `right_only`).
2. **Cardinality Verification (`validate=...`)**: Catch unexpected duplicate keys before propagation (`1:1`, `1:m`, `m:1`).
3. **Index Joins (`.join`)**: Direct joining on DataFrame indexes with automatic collision suffixes.
4. **Time-Series Asof Alignment (`pd.merge_asof`)**: Precise nearest backward/forward matching for asynchronous timestamps (e.g. trading ticks, telemetry sensors).

---

## Running Demonstrations

Run all Join demonstrations:
```bash
python3 -m pandas_lib.joins.run_examples --demo all
```

Or run targeted operations:
```bash
python3 -m pandas_lib.joins.run_examples --demo relational
python3 -m pandas_lib.joins.run_examples --demo index
python3 -m pandas_lib.joins.run_examples --demo concat
python3 -m pandas_lib.joins.run_examples --demo asof
```
