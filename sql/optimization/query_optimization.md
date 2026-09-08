# SQL Query Optimization & Indexing Reference

Techniques for analyzing execution plans, designing indexes, and eliminating query performance anti-patterns.

---

## 1. Execution Plan Analysis

Before optimizing, inspect the database query planner's actual execution path.

```sql
-- SQLite
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 42 AND status = 'shipped';

-- PostgreSQL
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE customer_id = 42 AND status = 'shipped';
```

Look for:
- `SCAN TABLE` (Full table scan — high I/O cost on large tables)
- `SEARCH TABLE ... USING INDEX` (Optimal index lookup)
- `TEMPORARY B-TREE FOR ORDER BY` (In-memory sorting due to lack of index ordering)

---

## 2. Indexing Best Practices

### Composite Indexes & Leftmost Prefix Rule
When querying on multiple columns (e.g., `WHERE tenant_id = 1 AND status = 'active' ORDER BY created_at DESC`), create a multi-column index:

```sql
CREATE INDEX idx_orders_tenant_status_date 
ON orders (tenant_id, status, created_at DESC);
```

> **Leftmost Prefix Rule**: An index on `(A, B, C)` accelerates queries filtering on `(A)`, `(A, B)`, and `(A, B, C)`. It **cannot** be used alone for queries filtering only on `(B)` or `(C)`.

### Covering Index (Index-Only Scan)
Include all projected columns in the index to completely avoid reading the table heap pages:

```sql
CREATE INDEX idx_orders_lookup 
ON orders (customer_id, status, total_amount);
```

---

## 3. Query Anti-Patterns to Avoid

| Anti-Pattern | Why It Hurts Performance | Recommended Fix |
|--------------|---------------------------|-----------------|
| `SELECT *` | Increases network payload, memory usage, prevents index-only scans. | Project only required columns: `SELECT id, total_amount`. |
| `WHERE YEAR(date_col) = 2026` | Wraps indexed column in a function, breaking sargability and forcing a full scan. | Use range bounds: `WHERE date_col >= '2026-01-01' AND date_col < '2027-01-01'`. |
| `WHERE name LIKE '%smith'` | Leading wildcard prevents B-Tree index range traversal. | Use suffix matching / full-text search index or trigram indexes. |
| `SELECT DISTINCT` to fix duplicate joins | Hides Cartesian products; forces expensive sorting/hash deduplication. | Correct the join conditions or use `EXISTS`. |
| `WHERE status != 'closed'` | Negative conditions (`!=`, `<>`) cannot leverage index range scanning. | Rewrite as positive equality: `WHERE status IN ('pending', 'active')`. |
