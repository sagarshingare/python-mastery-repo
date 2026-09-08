# SQL Fundamentals

> **Learning Path**: [Stage 04: SQL & Relational Databases](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-04-sql--relational-databases-sql) — **Step 4.1** (Prerequisite: [Stage 01: Core Python](file:///Users/sagarshingare/Documents/python-mastery-repo/core_python))

Core relational database mechanics: DDL schema design with constraint enforcement, DML CRUD operations, dynamic filtering predicates, aggregations with `GROUP BY / HAVING`, and cursor pagination.

---

## Key Concepts & Operations

1. **DDL Schema Design**: Primary keys, foreign key constraints (`PRAGMA foreign_keys = ON`), checks (`CHECK (salary >= 0)`), and unique indexes.
2. **DML CRUD**: Single and batch inserts (`executemany`), parameterized updates, and predicate-driven deletions.
3. **Filtering & Slicing**: Composing multi-clause predicates (`IN`, `BETWEEN`, `LIKE`, `IS NOT NULL`).
4. **Aggregations & Grouping**: Departmental salary calculations, headcount metrics, and post-aggregation filtering with `HAVING`.
5. **Pagination**: Stable ordered result retrieval using `ORDER BY`, `LIMIT`, and `OFFSET`.

---

## Running Demonstrations

Run all fundamentals demonstrations:
```bash
python3 -m sql.basics.run_examples --demo all
```

Or run targeted demonstrations:
```bash
python3 -m sql.basics.run_examples --demo crud
python3 -m sql.basics.run_examples --demo filtering
python3 -m sql.basics.run_examples --demo aggregation
python3 -m sql.basics.run_examples --demo pagination
```
