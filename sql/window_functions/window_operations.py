"""SQL Window Functions: Analytical ranking, Lead/Lag comparisons, and moving window frames."""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, List


def create_connection() -> sqlite3.Connection:
    """Create an in-memory SQLite connection."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_window_db(conn: sqlite3.Connection) -> None:
    """Initialize relational schema and seed time-series/department records."""
    cursor = conn.cursor()
    cursor.executescript(
        """
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department_id INTEGER,
            salary REAL NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        );

        CREATE TABLE monthly_revenue (
            sales_month TEXT PRIMARY KEY,
            revenue REAL NOT NULL
        );

        INSERT INTO departments (id, name) VALUES
            (1, 'Engineering'),
            (2, 'Product');

        INSERT INTO employees (id, name, department_id, salary) VALUES
            (1, 'Ada Lovelace', 1, 150000.0),
            (2, 'Grace Hopper', 1, 140000.0),
            (3, 'Alan Turing', 1, 140000.0),
            (4, 'Barbara Liskov', 1, 120000.0),
            (5, 'Margaret Hamilton', 2, 145000.0),
            (6, 'John von Neumann', 2, 130000.0),
            (7, 'Claude Shannon', 2, 115000.0);

        INSERT INTO monthly_revenue (sales_month, revenue) VALUES
            ('2026-01', 50000.0),
            ('2026-02', 58000.0),
            ('2026-03', 62000.0),
            ('2026-04', 60000.0),
            ('2026-05', 72000.0),
            ('2026-06', 75000.0);
        """
    )
    conn.commit()


def get_ranking_metrics(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Execute analytical ranking functions: ROW_NUMBER, RANK, DENSE_RANK, and NTILE."""
    query = """
        SELECT 
            e.id,
            e.name,
            d.name AS department_name,
            e.salary,
            ROW_NUMBER() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC, e.id ASC) AS row_num,
            RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS rank_pos,
            DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS dense_rank_pos,
            NTILE(2) OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS salary_half
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        ORDER BY e.department_id, e.salary DESC, e.id ASC;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_top_earners_per_dept(
    conn: sqlite3.Connection,
    top_n: int = 2,
) -> List[Dict[str, Any]]:
    """Retrieve top N highest earning employees per department using DENSE_RANK."""
    query = """
        WITH ranked_staff AS (
            SELECT 
                e.id,
                e.name,
                d.name AS department_name,
                e.salary,
                DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS rank_in_dept
            FROM employees e
            JOIN departments d ON e.department_id = d.id
        )
        SELECT id, name, department_name, salary, rank_in_dept
        FROM ranked_staff
        WHERE rank_in_dept <= ?
        ORDER BY department_name, rank_in_dept, salary DESC;
    """
    cursor = conn.cursor()
    cursor.execute(query, (top_n,))
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_month_over_month_growth(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Compute prior/next period values and MoM percentage growth via LAG and LEAD."""
    query = """
        SELECT 
            sales_month,
            revenue,
            LAG(revenue, 1) OVER (ORDER BY sales_month) AS prior_month_revenue,
            LEAD(revenue, 1) OVER (ORDER BY sales_month) AS next_month_revenue,
            ROUND(
                (revenue - LAG(revenue, 1, revenue) OVER (ORDER BY sales_month)) * 100.0 / 
                LAG(revenue, 1, revenue) OVER (ORDER BY sales_month),
                2
            ) AS mom_growth_pct
        FROM monthly_revenue
        ORDER BY sales_month;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_moving_aggregations(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Compute cumulative running totals and 3-month moving average window frames."""
    query = """
        SELECT 
            sales_month,
            revenue,
            SUM(revenue) OVER (
                ORDER BY sales_month
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS cumulative_revenue,
            ROUND(AVG(revenue) OVER (
                ORDER BY sales_month
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ), 2) AS moving_avg_3m
        FROM monthly_revenue
        ORDER BY sales_month;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
