"""Common Table Expressions (CTEs): Modular pipeline queries and recursive tree traversals."""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, List


def create_connection() -> sqlite3.Connection:
    """Create an in-memory SQLite connection."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_cte_db(conn: sqlite3.Connection) -> None:
    """Initialize tables and seed data for non-recursive and recursive CTEs."""
    cursor = conn.cursor()
    cursor.executescript(
        """
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            amount REAL NOT NULL,
            region TEXT NOT NULL
        );

        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            manager_id INTEGER,
            title TEXT NOT NULL,
            FOREIGN KEY (manager_id) REFERENCES employees(id)
        );

        INSERT INTO orders (order_id, customer_name, amount, region) VALUES
            (101, 'Acme Corp', 15000.0, 'North America'),
            (102, 'Globex Inc', 8000.0, 'North America'),
            (103, 'Soylent Corp', 12000.0, 'Europe'),
            (104, 'Initech', 3500.0, 'Europe'),
            (105, 'Umbrella Corp', 4500.0, 'Asia Pacific'),
            (106, 'Hooli', 5000.0, 'Asia Pacific'),
            (107, 'Massive Dynamic', 22000.0, 'North America');

        INSERT INTO employees (id, name, manager_id, title) VALUES
            (1, 'Ada Lovelace', NULL, 'Chief Executive Officer'),
            (2, 'Margaret Hamilton', 1, 'VP of Engineering'),
            (3, 'Alan Turing', 2, 'Principal Architect'),
            (4, 'Grace Hopper', 2, 'Director of Infrastructure'),
            (5, 'John von Neumann', 3, 'Senior Systems Engineer'),
            (6, 'Claude Shannon', 4, 'Senior Network Engineer');
        """
    )
    conn.commit()


def get_modular_pipeline_cte(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Execute modular non-recursive CTE finding orders from above-average performing regions."""
    query = """
        WITH regional_sales AS (
            SELECT region, SUM(amount) AS total_sales, COUNT(*) AS order_count
            FROM orders
            GROUP BY region
        ),
        sales_benchmark AS (
            SELECT AVG(total_sales) AS avg_regional_benchmark
            FROM regional_sales
        ),
        top_regions AS (
            SELECT rs.region, rs.total_sales, rs.order_count
            FROM regional_sales rs, sales_benchmark sb
            WHERE rs.total_sales > sb.avg_regional_benchmark
        )
        SELECT 
            o.order_id,
            o.customer_name,
            o.amount,
            o.region,
            tr.total_sales AS region_total
        FROM orders o
        JOIN top_regions tr ON o.region = tr.region
        ORDER BY o.amount DESC;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def generate_number_sequence(
    conn: sqlite3.Connection,
    start: int = 1,
    end: int = 10,
) -> List[int]:
    """Generate a contiguous integer sequence via recursive CTE."""
    query = """
        WITH RECURSIVE number_series(n) AS (
            SELECT ?
            UNION ALL
            SELECT n + 1 FROM number_series WHERE n < ?
        )
        SELECT n FROM number_series;
    """
    cursor = conn.cursor()
    cursor.execute(query, (start, end))
    return [row[0] for row in cursor.fetchall()]


def get_org_chart_hierarchy(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Execute recursive CTE traversing corporate reporting tree from CEO down."""
    query = """
        WITH RECURSIVE org_hierarchy AS (
            -- Anchor Member: Root executive (manager_id IS NULL)
            SELECT 
                id,
                name,
                manager_id,
                title,
                1 AS depth,
                name AS management_path
            FROM employees
            WHERE manager_id IS NULL

            UNION ALL

            -- Recursive Member: Subordinates joining to parent org_hierarchy
            SELECT 
                e.id,
                e.name,
                e.manager_id,
                e.title,
                o.depth + 1,
                o.management_path || ' -> ' || e.name
            FROM employees e
            JOIN org_hierarchy o ON e.manager_id = o.id
        )
        SELECT id, name, title, depth, management_path
        FROM org_hierarchy
        ORDER BY depth, id;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
