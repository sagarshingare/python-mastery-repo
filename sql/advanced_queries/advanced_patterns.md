# Advanced SQL Patterns Reference

Techniques for conditional aggregation (pivot), unpivoting, upserts, JSON querying, and gaps-and-islands analysis.

---

## 1. Pivoting via Conditional Aggregation

Transform rows into dynamic column metrics across categories without vendor-specific pivot extensions:

```sql
SELECT 
    department_id,
    SUM(CASE WHEN role = 'Engineer' THEN 1 ELSE 0 END) AS engineer_count,
    SUM(CASE WHEN role = 'Manager' THEN 1 ELSE 0 END) AS manager_count,
    SUM(CASE WHEN role = 'Designer' THEN 1 ELSE 0 END) AS designer_count,
    COUNT(*) AS total_staff
FROM employees
GROUP BY department_id;
```

---

## 2. Unpivoting Columns to Rows

Normalize wide metric tables into long key-value datasets:

```sql
SELECT product_id, 'Q1' AS quarter, q1_sales AS sales FROM quarterly_sales
UNION ALL
SELECT product_id, 'Q2' AS quarter, q2_sales AS sales FROM quarterly_sales
UNION ALL
SELECT product_id, 'Q3' AS quarter, q3_sales AS sales FROM quarterly_sales
UNION ALL
SELECT product_id, 'Q4' AS quarter, q4_sales AS sales FROM quarterly_sales;
```

---

## 3. Upsert Patterns (ON CONFLICT / MERGE)

Atomically insert a record or update existing values if the unique key already exists.

```sql
-- SQLite / PostgreSQL standard UPSERT
INSERT INTO user_preferences (user_id, theme, notifications_enabled, updated_at)
VALUES (42, 'dark', TRUE, CURRENT_TIMESTAMP)
ON CONFLICT (user_id) DO UPDATE SET
    theme = EXCLUDED.theme,
    notifications_enabled = EXCLUDED.notifications_enabled,
    updated_at = EXCLUDED.updated_at;
```

---

## 4. JSON Querying in SQL

Store flexible, semi-structured documents in relational databases:

```sql
-- Extract nested JSON attributes
SELECT 
    id,
    json_extract(metadata, '$.browser') AS browser,
    json_extract(metadata, '$.os.version') AS os_version
FROM access_logs
WHERE json_extract(metadata, '$.status') = 'success';
```

---

## 5. Gaps and Islands Problem

Detect contiguous streaks (islands) or missing intervals (gaps) in sequential event streams (e.g. consecutive daily logins).

```sql
WITH numbered_logins AS (
    SELECT 
        user_id,
        login_date,
        -- Subtract row number from date to produce an invariant grouping key
        date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS streak_group
    FROM user_daily_logins
)
SELECT 
    user_id,
    MIN(login_date) AS streak_start,
    MAX(login_date) AS streak_end,
    COUNT(*) AS consecutive_days
FROM numbered_logins
GROUP BY user_id, streak_group
HAVING COUNT(*) >= 3
ORDER BY consecutive_days DESC;
```
