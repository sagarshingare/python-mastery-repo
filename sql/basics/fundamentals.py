"""SQL Fundamentals: DDL, DML, filtering, aggregation, and pagination operations."""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Optional, Tuple


def create_connection() -> sqlite3.Connection:
    """Create an in-memory SQLite connection with foreign keys enabled."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_fundamentals_db(conn: sqlite3.Connection) -> None:
    """Initialize relational schema with constraints and seed data."""
    cursor = conn.cursor()
    cursor.executescript(
        """
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department_id INTEGER,
            salary REAL NOT NULL CHECK (salary >= 0),
            hire_date TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        );

        INSERT INTO departments (id, name) VALUES
            (1, 'Engineering'),
            (2, 'Product'),
            (3, 'Marketing');

        INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date, is_active) VALUES
            ('Ada', 'Lovelace', 'ada@example.com', 1, 150000.0, '2021-01-15', 1),
            ('Alan', 'Turing', 'alan@example.com', 1, 130000.0, '2021-06-01', 1),
            ('Grace', 'Hopper', 'grace@example.com', 1, 135000.0, '2022-03-10', 1),
            ('Margaret', 'Hamilton', 'margaret@example.com', 2, 140000.0, '2022-07-20', 1),
            ('John', 'von Neumann', 'john@example.com', 2, 125000.0, '2023-02-14', 1),
            ('Claude', 'Shannon', 'claude@example.com', 3, 110000.0, '2023-09-01', 0);
        """
    )
    conn.commit()


def insert_employee(
    conn: sqlite3.Connection,
    first_name: str,
    last_name: str,
    email: str,
    department_id: Optional[int],
    salary: float,
    hire_date: str,
    is_active: bool = True,
) -> int:
    """Insert a single employee record and return generated ID."""
    query = """
        INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    cursor = conn.cursor()
    cursor.execute(
        query,
        (first_name, last_name, email, department_id, salary, hire_date, 1 if is_active else 0),
    )
    conn.commit()
    return cursor.lastrowid  # type: ignore[return-value]


def batch_insert_employees(
    conn: sqlite3.Connection,
    records: List[Tuple[str, str, str, Optional[int], float, str, int]],
) -> int:
    """Batch insert multiple employee records via executemany."""
    query = """
        INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    cursor = conn.cursor()
    cursor.executemany(query, records)
    conn.commit()
    return cursor.rowcount


def update_employee_salary(
    conn: sqlite3.Connection,
    department_id: int,
    multiplier: float,
) -> int:
    """Update salaries for active employees in a given department."""
    query = """
        UPDATE employees
        SET salary = ROUND(salary * ?, 2)
        WHERE department_id = ? AND is_active = 1;
    """
    cursor = conn.cursor()
    cursor.execute(query, (multiplier, department_id))
    conn.commit()
    return cursor.rowcount


def delete_inactive_employees(
    conn: sqlite3.Connection,
    hire_date_before: str,
) -> int:
    """Delete inactive employees hired prior to specified cutoff date."""
    query = """
        DELETE FROM employees
        WHERE is_active = 0 AND hire_date < ?;
    """
    cursor = conn.cursor()
    cursor.execute(query, (hire_date_before,))
    conn.commit()
    return cursor.rowcount


def filter_employees(
    conn: sqlite3.Connection,
    department_ids: Optional[List[int]] = None,
    min_salary: Optional[float] = None,
    max_salary: Optional[float] = None,
    email_domain: Optional[str] = None,
    active_only: bool = True,
) -> List[Dict[str, Any]]:
    """Execute dynamic predicate filtering on employees."""
    conditions = []
    params: List[Any] = []

    if active_only:
        conditions.append("is_active = 1")
    if department_ids:
        placeholders = ",".join("?" * len(department_ids))
        conditions.append(f"department_id IN ({placeholders})")
        params.extend(department_ids)
    if min_salary is not None:
        conditions.append("salary >= ?")
        params.append(min_salary)
    if max_salary is not None:
        conditions.append("salary <= ?")
        params.append(max_salary)
    if email_domain:
        conditions.append("email LIKE ?")
        params.append(f"%@{email_domain}")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"""
        SELECT id, first_name, last_name, email, department_id, salary, hire_date, is_active
        FROM employees
        {where_clause}
        ORDER BY salary DESC;
    """
    cursor = conn.cursor()
    cursor.execute(query, params)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_department_metrics(
    conn: sqlite3.Connection,
    min_headcount: int = 1,
) -> List[Dict[str, Any]]:
    """Compute aggregated metrics (headcount, avg/min/max salary) per department."""
    query = """
        SELECT 
            COALESCE(d.name, 'Unassigned') AS department_name,
            COUNT(e.id) AS employee_count,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            MIN(e.salary) AS min_salary,
            MAX(e.salary) AS max_salary
        FROM departments d
        LEFT JOIN employees e ON d.id = e.department_id AND e.is_active = 1
        GROUP BY d.id, d.name
        HAVING COUNT(e.id) >= ?
        ORDER BY avg_salary DESC;
    """
    cursor = conn.cursor()
    cursor.execute(query, (min_headcount,))
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def paginate_employees(
    conn: sqlite3.Connection,
    page: int = 1,
    page_size: int = 2,
    active_only: bool = True,
) -> Tuple[int, List[Dict[str, Any]]]:
    """Fetch paginated employees using LIMIT and OFFSET, returning (total_count, rows)."""
    offset = max(0, (page - 1) * page_size)
    filter_sql = "WHERE is_active = 1" if active_only else ""

    count_cursor = conn.cursor()
    count_cursor.execute(f"SELECT COUNT(*) FROM employees {filter_sql};")
    total_count: int = count_cursor.fetchone()[0]

    data_cursor = conn.cursor()
    data_cursor.execute(
        f"""
        SELECT id, first_name || ' ' || last_name AS full_name, email, salary, hire_date
        FROM employees
        {filter_sql}
        ORDER BY salary DESC, hire_date ASC
        LIMIT ? OFFSET ?;
        """,
        (page_size, offset),
    )
    columns = [col[0] for col in data_cursor.description]
    rows = [dict(zip(columns, row)) for row in data_cursor.fetchall()]
    return total_count, rows
