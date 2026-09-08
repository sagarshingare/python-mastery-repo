# SQL Join Patterns Reference

Relational joining techniques: INNER, LEFT, RIGHT, FULL, CROSS, SELF, and anti-joins.

---

## Data Model Example

```sql
-- departments table
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- employees table
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    department_id INTEGER,
    manager_id INTEGER
);
```

---

## 1. INNER JOIN

Returns rows when there is a match in **both** tables.

```sql
SELECT 
    e.name AS employee_name,
    d.name AS department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;
```

---

## 2. LEFT OUTER JOIN

Returns **all rows from the left table**, and matched rows from the right table. Unmatched right columns contain `NULL`.

```sql
SELECT 
    e.name AS employee_name,
    COALESCE(d.name, 'Unassigned') AS department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id;
```

---

## 3. RIGHT OUTER JOIN

Returns **all rows from the right table**, and matched rows from the left table.

```sql
SELECT 
    d.name AS department_name,
    e.name AS employee_name
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.id;
```

*(Note: In databases lacking native `RIGHT JOIN` like SQLite, swap table positions in a `LEFT JOIN`)*

---

## 4. FULL OUTER JOIN

Returns rows when there is a match in **either** the left or the right table.

```sql
-- Standard SQL
SELECT 
    e.name AS employee_name,
    d.name AS department_name
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.id;

-- SQLite equivalent using UNION ALL
SELECT e.name, d.name FROM employees e LEFT JOIN departments d ON e.department_id = d.id
UNION
SELECT e.name, d.name FROM departments d LEFT JOIN employees e ON d.id = e.department_id;
```

---

## 5. ANTI-JOIN (Finding Unmatched Records)

Identify employees without departments, or departments with zero employees.

```sql
-- Departments with NO employees assigned
SELECT d.id, d.name
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
WHERE e.id IS NULL;
```

---

## 6. SELF JOIN (Hierarchical Data)

Joining a table to itself using aliases to resolve hierarchical relationships like employee-manager.

```sql
SELECT 
    emp.name AS employee,
    COALESCE(mgr.name, 'Top Level Executive') AS manager
FROM employees emp
LEFT JOIN employees mgr ON emp.manager_id = mgr.id;
```

---

## 7. CROSS JOIN (Cartesian Product)

Pairs every row from table A with every row from table B. Often used for matrix generation.

```sql
SELECT 
    p.product_code,
    s.size_name
FROM products p
CROSS JOIN sizes s;
```
