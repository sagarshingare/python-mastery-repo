# Common Table Expressions (CTEs)

> **Learning Path**: [Stage 04: SQL & Relational Databases](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-04-sql--relational-databases-sql) — **Step 4.3** (Prerequisite: [Step 4.2: Join Patterns](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/joins))

Modular SQL pipeline authoring with non-recursive and recursive `WITH` clauses: breaking complex joins into readable stages, generating series dynamically, and traversing hierarchical tree structures.

---

## CTE Architectural Paradigms

1. **Modular Non-Recursive Pipeline**: Break complex multi-join queries into sequential stages (`regional_sales -> sales_benchmark -> top_regions -> final select`).
2. **Recursive Series Generation**: Synthesize integer sequences or date calendars on-the-fly without persistent number tables.
3. **Recursive Graph/Tree Traversal**: Traverse parent-child relationships (e.g., employee to manager) calculating node depth and cumulative reporting paths.

---

## Running Demonstrations

Run all CTE demonstrations:
```bash
python3 -m sql.cte.run_examples --demo all
```

Or run targeted demonstrations:
```bash
python3 -m sql.cte.run_examples --demo modular
python3 -m sql.cte.run_examples --demo sequence
python3 -m sql.cte.run_examples --demo hierarchy
```
