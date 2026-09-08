# Advanced SQL Patterns

> **Learning Path**: [Stage 04: SQL & Relational Databases](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-04-sql--relational-databases-sql) — **Step 4.5** (Prerequisite: [Step 4.4: Window Functions](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/window_functions))

Techniques for conditional aggregation pivoting, column unpivoting via `UNION ALL`, atomic idempotency via `UPSERT` (`ON CONFLICT ... DO UPDATE`), semi-structured document querying with `json_extract`, and Gaps & Islands contiguous sequence detection.

---

## Pattern Matrix

| Pattern | SQL Construct | Business Problem Solved |
|:---|:---|:---|
| **Pivot** | `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` | Matrix reports, dynamic metric aggregation by category |
| **Unpivot** | `UNION ALL` across columns | Normalizing legacy wide spreadsheets into long relational models |
| **Atomic UPSERT** | `ON CONFLICT (key) DO UPDATE` | Idempotent data ingestion pipelines, user preference updates |
| **JSON Querying** | `json_extract(col, '$.path')` | Querying dynamic metadata payloads, schemaless extension fields |
| **Gaps & Islands** | `date - ROW_NUMBER()` | Continuous usage streak analysis, event sequence grouping |

---

## Running Demonstrations

Run all Advanced SQL demonstrations:
```bash
python3 -m sql.advanced_queries.run_examples --demo all
```

Or run targeted demonstrations:
```bash
python3 -m sql.advanced_queries.run_examples --demo pivot
python3 -m sql.advanced_queries.run_examples --demo unpivot
python3 -m sql.advanced_queries.run_examples --demo upsert
python3 -m sql.advanced_queries.run_examples --demo json
python3 -m sql.advanced_queries.run_examples --demo gaps_islands
```
