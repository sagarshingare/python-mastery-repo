"""Advanced SQL Patterns: Conditional pivot, unpivoting, atomic UPSERT, JSON extraction, and Gaps & Islands."""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Dict, List, Optional


def create_connection() -> sqlite3.Connection:
    """Create an in-memory SQLite connection."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_advanced_db(conn: sqlite3.Connection) -> None:
    """Initialize test tables and seed data for advanced query patterns."""
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
            role TEXT NOT NULL,
            metadata TEXT NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        );

        CREATE TABLE quarterly_sales (
            product_id TEXT PRIMARY KEY,
            q1_sales REAL NOT NULL,
            q2_sales REAL NOT NULL,
            q3_sales REAL NOT NULL,
            q4_sales REAL NOT NULL
        );

        CREATE TABLE user_preferences (
            user_id INTEGER PRIMARY KEY,
            theme TEXT NOT NULL,
            notifications_enabled INTEGER NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE user_daily_logins (
            user_id INTEGER NOT NULL,
            login_date TEXT NOT NULL,
            PRIMARY KEY (user_id, login_date)
        );

        INSERT INTO departments (id, name) VALUES
            (1, 'Engineering'),
            (2, 'Product');

        INSERT INTO employees (id, name, department_id, role, metadata) VALUES
            (1, 'Ada Lovelace', 1, 'Engineer', '{"level": "principal", "location": "Remote", "skills": ["Python", "C++"]}'),
            (2, 'Grace Hopper', 1, 'Engineer', '{"level": "lead", "location": "New York", "skills": ["Compilers", "Python"]}'),
            (3, 'Alan Turing', 1, 'Engineer', '{"level": "senior", "location": "London", "skills": ["Cryptography", "Algorithms"]}'),
            (4, 'Margaret Hamilton', 2, 'Manager', '{"level": "director", "location": "Boston", "skills": ["Systems", "Management"]}'),
            (5, 'John von Neumann', 2, 'Designer', '{"level": "senior", "location": "Remote", "skills": ["Architecture", "UI"]}');

        INSERT INTO quarterly_sales VALUES
            ('PROD-ALPHA', 12000.0, 15000.0, 18000.0, 22000.0),
            ('PROD-BETA', 8500.0, 9200.0, 7800.0, 11000.0);

        INSERT INTO user_preferences VALUES
            (42, 'dark', 1, '2026-01-01 10:00:00');

        -- Consecutive logins for Gaps and Islands analysis:
        -- User 101 has a 4-day streak (2026-03-01 to 2026-03-04) and a 1-day login on 2026-03-10
        -- User 102 has sporadic logins (2026-03-01, 2026-03-03, 2026-03-05)
        INSERT INTO user_daily_logins VALUES
            (101, '2026-03-01'),
            (101, '2026-03-02'),
            (101, '2026-03-03'),
            (101, '2026-03-04'),
            (101, '2026-03-10'),
            (102, '2026-03-01'),
            (102, '2026-03-03'),
            (102, '2026-03-05');
        """
    )
    conn.commit()


def pivot_role_headcount(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Execute conditional aggregation to pivot department headcount metrics by role."""
    query = """
        SELECT 
            d.name AS department_name,
            SUM(CASE WHEN e.role = 'Engineer' THEN 1 ELSE 0 END) AS engineers,
            SUM(CASE WHEN e.role = 'Manager' THEN 1 ELSE 0 END) AS managers,
            SUM(CASE WHEN e.role = 'Designer' THEN 1 ELSE 0 END) AS designers,
            COUNT(e.id) AS total_headcount
        FROM departments d
        LEFT JOIN employees e ON d.id = e.department_id
        GROUP BY d.id, d.name
        ORDER BY total_headcount DESC;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def unpivot_quarterly_sales(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Unpivot wide columns to normalized rows via UNION ALL."""
    query = """
        SELECT product_id, 'Q1' AS quarter, q1_sales AS amount FROM quarterly_sales
        UNION ALL
        SELECT product_id, 'Q2' AS quarter, q2_sales AS amount FROM quarterly_sales
        UNION ALL
        SELECT product_id, 'Q3' AS quarter, q3_sales AS amount FROM quarterly_sales
        UNION ALL
        SELECT product_id, 'Q4' AS quarter, q4_sales AS amount FROM quarterly_sales
        ORDER BY product_id, quarter;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def upsert_user_preference(
    conn: sqlite3.Connection,
    user_id: int,
    theme: str,
    notifications_enabled: bool,
    updated_at: str,
) -> None:
    """Execute atomic UPSERT (ON CONFLICT ... DO UPDATE)."""
    query = """
        INSERT INTO user_preferences (user_id, theme, notifications_enabled, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT (user_id) DO UPDATE SET
            theme = EXCLUDED.theme,
            notifications_enabled = EXCLUDED.notifications_enabled,
            updated_at = EXCLUDED.updated_at;
    """
    cursor = conn.cursor()
    cursor.execute(
        query,
        (user_id, theme, 1 if notifications_enabled else 0, updated_at),
    )
    conn.commit()


def get_user_preference(conn: sqlite3.Connection, user_id: int) -> Optional[Dict[str, Any]]:
    """Fetch user preference by primary key."""
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, theme, notifications_enabled, updated_at FROM user_preferences WHERE user_id = ?;", (user_id,))
    row = cursor.fetchone()
    if not row:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def query_json_metadata(
    conn: sqlite3.Connection,
    min_level: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Extract and filter semi-structured JSON attributes via json_extract."""
    levels = min_level or ["principal", "lead", "director"]
    placeholders = ",".join("?" * len(levels))
    query = f"""
        SELECT 
            id,
            name,
            role,
            json_extract(metadata, '$.level') AS seniority_level,
            json_extract(metadata, '$.location') AS location,
            json_extract(metadata, '$.skills[0]') AS primary_skill
        FROM employees
        WHERE json_extract(metadata, '$.level') IN ({placeholders})
        ORDER BY seniority_level;
    """
    cursor = conn.cursor()
    cursor.execute(query, levels)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def detect_gaps_and_islands(
    conn: sqlite3.Connection,
    min_streak_days: int = 3,
) -> List[Dict[str, Any]]:
    """Identify contiguous login streaks (islands) using the row-number difference technique."""
    query = """
        WITH numbered_logins AS (
            SELECT 
                user_id,
                login_date,
                date(login_date, '-' || ROW_NUMBER() OVER (
                    PARTITION BY user_id ORDER BY login_date
                ) || ' days') AS streak_island_group
            FROM user_daily_logins
        )
        SELECT 
            user_id,
            MIN(login_date) AS streak_start,
            MAX(login_date) AS streak_end,
            COUNT(*) AS consecutive_days
        FROM numbered_logins
        GROUP BY user_id, streak_island_group
        HAVING COUNT(*) >= ?
        ORDER BY user_id, streak_start;
    """
    cursor = conn.cursor()
    cursor.execute(query, (min_streak_days,))
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
