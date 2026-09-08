# SQL Fundamentals Reference

A complete guide to core SQL operations: DDL, DML, filtering, aggregation, and sorting.

---

## 1. Table Creation (DDL)

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INTEGER,
    salary NUMERIC(10, 2) NOT NULL CHECK (salary >= 0),
    hire_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
```

---

## 2. Basic CRUD Operations (DML)

### Insert Records
```sql
-- Single row insert
INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
VALUES ('Alice', 'Smith', 'alice@example.com', 1, 85000.00, '2022-03-15');

-- Multi-row batch insert
INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
VALUES 
    ('Bob', 'Jones', 'bob@example.com', 2, 72000.00, '2023-01-10'),
    ('Charlie', 'Brown', 'charlie@example.com', 1, 95000.00, '2021-08-01');
```

### Query Records (SELECT)
```sql
-- Projection with column aliasing
SELECT 
    first_name || ' ' || last_name AS full_name,
    salary,
    ROUND(salary * 0.10, 2) AS estimated_bonus
FROM employees;
```

### Update Records
```sql
-- Safe update with WHERE predicate
UPDATE employees
SET salary = salary * 1.05
WHERE department_id = 1 AND is_active = TRUE;
```

### Delete Records
```sql
-- Targeted deletion
DELETE FROM employees
WHERE is_active = FALSE AND hire_date < '2020-01-01';
```

---

## 3. Filtering & Predicates

```sql
SELECT * FROM employees
WHERE department_id IN (1, 2, 3)
  AND salary BETWEEN 60000 AND 100000
  AND email LIKE '%@example.com'
  AND is_active IS NOT NULL;
```

---

## 4. Aggregations & Grouping

```sql
-- Compute department salary metrics
SELECT 
    department_id,
    COUNT(*) AS employee_count,
    ROUND(AVG(salary), 2) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary
FROM employees
WHERE is_active = TRUE
GROUP BY department_id
HAVING COUNT(*) >= 2
ORDER BY avg_salary DESC;
```

---

## 5. Sorting and Pagination

```sql
-- Fetch page 2 of top-earning active employees (10 records per page)
SELECT id, first_name, last_name, salary
FROM employees
WHERE is_active = TRUE
ORDER BY salary DESC, hire_date ASC
LIMIT 10 OFFSET 10;
```
