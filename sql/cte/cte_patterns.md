# Common Table Expressions (CTE) Reference

Modular SQL development with non-recursive and recursive `WITH` clauses.

---

## 1. Why Use CTEs?

- **Readability**: Break deeply nested subqueries into sequential, named pipeline stages.
- **Reusability**: Reference the same named CTE multiple times in the primary query.
- **Recursion**: Traverse trees, graphs, hierarchical org charts, and generate sequences.

---

## 2. Standard Non-Recursive CTE

```sql
WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM orders
    GROUP BY region
),
top_regions AS (
    SELECT region
    FROM regional_sales
    WHERE total_sales > (SELECT AVG(total_sales) FROM regional_sales)
)
SELECT 
    o.order_id, 
    o.customer_name, 
    o.amount, 
    o.region
FROM orders o
WHERE o.region IN (SELECT region FROM top_regions);
```

---

## 3. Recursive CTE: Number Series Generation

Generate a date range or sequence of integers without an explicit table.

```sql
WITH RECURSIVE numbers(n) AS (
    -- Anchor member
    SELECT 1
    UNION ALL
    -- Recursive member
    SELECT n + 1 FROM numbers WHERE n < 10
)
SELECT n FROM numbers;
```

---

## 4. Recursive CTE: Organizational Hierarchy Traversal

Traverse an employee-manager tree from the CEO down, calculating employee level/depth.

```sql
WITH RECURSIVE org_hierarchy AS (
    -- Anchor: CEO (manager_id IS NULL)
    SELECT 
        id, 
        name, 
        manager_id, 
        1 AS org_level, 
        CAST(name AS TEXT) AS management_chain
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive: Reportees joining back to prior level
    SELECT 
        e.id, 
        e.name, 
        e.manager_id, 
        h.org_level + 1,
        h.management_chain || ' -> ' || e.name
    FROM employees e
    INNER JOIN org_hierarchy h ON e.manager_id = h.id
)
SELECT * FROM org_hierarchy
ORDER BY org_level, name;
```
