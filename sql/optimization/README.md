# SQL Query Optimization & Indexing

> **Learning Path**: [Stage 04: SQL & Relational Databases](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-04-sql--relational-databases-sql) — **Step 4.6** (Prerequisite: [Step 4.5: Advanced Queries](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/advanced_queries))

Techniques for database execution plan analysis, B-Tree index design, leftmost prefix rules on composite indexes, and eliminating query performance anti-patterns via sargable refactoring.

---

## Performance Rules & Best Practices

1. **Plan Inspection**: Use `EXPLAIN QUERY PLAN` to differentiate between full table scans (`SCAN orders`) and indexed lookups (`SEARCH orders USING INDEX`).
2. **Composite Leftmost Prefix Rule**: Multi-column index `(A, B)` accelerates queries filtering on `(A)` and `(A, B)`, but **not** queries filtering solely on `(B)`.
3. **Sargability**: Avoid wrapping indexed columns in functions (e.g. `SUBSTR(date_col, 1, 7) = '2026-05'`). Instead, express predicates using direct comparison ranges (`date_col >= '2026-05-01' AND date_col < '2026-06-01'`).
4. **Covering Indexes**: Project only columns present in the index to enable index-only scans without table heap access.

---

## Running Demonstrations

Run all Query Optimization demonstrations:
```bash
python3 -m sql.optimization.run_examples --demo all
```

Or run targeted demonstrations:
```bash
python3 -m sql.optimization.run_examples --demo explain
python3 -m sql.optimization.run_examples --demo indexing
python3 -m sql.optimization.run_examples --demo composite
python3 -m sql.optimization.run_examples --demo sargability
```
