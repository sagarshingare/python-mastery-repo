"""SQL Join Operations: INNER, LEFT, ANTI-JOIN, SELF-JOIN, CROSS JOIN, and simulated FULL OUTER JOIN."""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, List


def create_connection() -> sqlite3.Connection:
    """Create an in-memory SQLite connection."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_joins_db(conn: sqlite3.Connection) -> None:
    """Initialize test tables and seed data for relational joins."""
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
            manager_id INTEGER,
            salary REAL NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            product_code TEXT NOT NULL
        );

        CREATE TABLE sizes (
            id INTEGER PRIMARY KEY,
            size_name TEXT NOT NULL
        );

        INSERT INTO departments (id, name) VALUES
            (1, 'Engineering'),
            (2, 'Product'),
            (3, 'Marketing'),
            (4, 'Unused Operations');

        INSERT INTO employees (id, name, department_id, manager_id, salary) VALUES
            (1, 'Ada Lovelace', 1, NULL, 150000.0),
            (2, 'Alan Turing', 1, 1, 130000.0),
            (3, 'Margaret Hamilton', 2, 1, 140000.0),
            (4, 'Contractor Dan', NULL, NULL, 60000.0);

        INSERT INTO products (id, product_code) VALUES
            (1, 'TSHIRT-01'),
            (2, 'HOODIE-02');

        INSERT INTO sizes (id, size_name) VALUES
            (1, 'Small'),
            (2, 'Medium'),
            (3, 'Large');
        """
    )
    conn.commit()


def get_inner_join_records(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Execute INNER JOIN returning only employees with matching departments."""
    query = """
        SELECT 
            e.id AS employee_id,
            e.name AS employee_name,
            d.name AS department_name,
            e.salary
        FROM employees e
        INNER JOIN departments d ON e.department_id = d.id
        ORDER BY e.id;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_left_join_records(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Execute LEFT OUTER JOIN including employees without assigned departments."""
    query = """
        SELECT 
            e.id AS employee_id,
            e.name AS employee_name,
            COALESCE(d.name, 'Unassigned') AS department_name,
            e.salary
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        ORDER BY e.id;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_anti_join_departments(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Execute ANTI-JOIN to find departments with zero assigned employees."""
    query = """
        SELECT 
            d.id AS department_id,
            d.name AS department_name
        FROM departments d
        LEFT JOIN employees e ON d.id = e.department_id
        WHERE e.id IS NULL
        ORDER BY d.id;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_self_join_hierarchy(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Execute SELF JOIN on employees table to resolve manager names."""
    query = """
        SELECT 
            emp.id AS employee_id,
            emp.name AS employee_name,
            COALESCE(mgr.name, 'Top Executive / Self') AS manager_name
        FROM employees emp
        LEFT JOIN employees mgr ON emp.manager_id = mgr.id
        ORDER BY emp.id;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_cross_join_combinations(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Execute CROSS JOIN producing Cartesian product of products and sizes."""
    query = """
        SELECT 
            p.product_code,
            s.size_name,
            p.product_code || '-' || UPPER(SUBSTR(s.size_name, 1, 1)) AS sku
        FROM products p
        CROSS JOIN sizes s
        ORDER BY p.id, s.id;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_full_outer_join_simulation(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Simulate FULL OUTER JOIN via UNION of LEFT JOIN and RIGHT/Anti-Join."""
    query = """
        SELECT e.name AS employee_name, d.name AS department_name
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        UNION
        SELECT e.name AS employee_name, d.name AS department_name
        FROM departments d
        LEFT JOIN employees e ON d.id = e.department_id
        ORDER BY employee_name, department_name;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
