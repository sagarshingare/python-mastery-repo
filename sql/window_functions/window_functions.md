# SQL Window Functions Reference

Advanced analytical queries using `OVER (PARTITION BY ... ORDER BY ...)`.

---

## 1. Syntax Anatomy

```sql
function_name([expression]) OVER (
    [PARTITION BY partition_column_1, ...]
    [ORDER BY sort_column_1 [ASC | DESC], ...]
    [ROWS | RANGE BETWEEN frame_start AND frame_end]
)
```

---

## 2. Ranking Functions

| Function | Behavior |
|----------|----------|
| `ROW_NUMBER()` | Assigns a strictly unique sequential integer starting at 1. |
| `RANK()` | Assigns same rank to tied values; skips subsequent ranks (1, 2, 2, 4). |
| `DENSE_RANK()` | Assigns same rank to tied values; does not skip ranks (1, 2, 2, 3). |
| `NTILE(k)` | Divides sorted rows into `k` roughly equal buckets (e.g. quartiles). |

### Example: Top 2 Earners Per Department
```sql
WITH ranked_employees AS (
    SELECT 
        id,
        first_name,
        last_name,
        department_id,
        salary,
        DENSE_RANK() OVER (
            PARTITION BY department_id 
            ORDER BY salary DESC
        ) AS rank_in_dept
    FROM employees
)
SELECT * FROM ranked_employees
WHERE rank_in_dept <= 2;
```

---

## 3. Lead and Lag (Time Series & Prior Row Comparisons)

### Example: Month-Over-Month Revenue Growth
```sql
SELECT 
    sales_month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY sales_month) AS prior_month_revenue,
    ROUND(
        (revenue - LAG(revenue, 1) OVER (ORDER BY sales_month)) * 100.0 / 
        LAG(revenue, 1) OVER (ORDER BY sales_month), 
        2
    ) AS mom_growth_pct
FROM monthly_sales;
```

---

## 4. Running Totals & Cumulative Aggregates

```sql
SELECT 
    transaction_date,
    amount,
    -- Running total across the entire account history
    SUM(amount) OVER (
        ORDER BY transaction_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_balance,
    -- 7-day moving average
    AVG(amount) OVER (
        ORDER BY transaction_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_7d_avg
FROM account_transactions;
```
