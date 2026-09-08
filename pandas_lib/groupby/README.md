# Pandas GroupBy Operations

> **Learning Path**: [Stage 05: Data Analytics & Scientific Libraries](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) — **Step 5.2**

Split-Apply-Combine patterns using Pandas: multi-metric named aggregations, row-preserving transformations (z-scores, percentage of group total), group-level filtering, and multi-dimensional pivot tables.

---

## Key Operations

1. **Named Aggregations (`.agg`)**: Clean, descriptive column output avoiding awkward MultiIndex column hierarchies.
2. **Transformations (`.transform`)**: Group-level metrics broadcast back to individual rows without altering DataFrame length.
3. **Filtering (`.filter`)**: Selective pruning of groups based on aggregate conditions (e.g. minimum count or total threshold).
4. **Pivoting (`pd.pivot_table`)**: Reshaping datasets with multiple dimensions and marginal sum summaries.

---

## Running Demonstrations

Run all GroupBy demonstrations:
```bash
python3 -m pandas_lib.groupby.run_examples --demo all
```

Or run individual patterns:
```bash
python3 -m pandas_lib.groupby.run_examples --demo agg
python3 -m pandas_lib.groupby.run_examples --demo transform
python3 -m pandas_lib.groupby.run_examples --demo filter
python3 -m pandas_lib.groupby.run_examples --demo pivot
```
