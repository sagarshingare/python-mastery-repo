"""SQL Query Optimization: EXPLAIN QUERY PLAN analysis, B-Tree indexing, and sargability."""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Tuple


def create_connection() -> sqlite3.Connection:
    """Create an in-memory SQLite connection."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_optimization_db(conn: sqlite3.Connection) -> None:
    """Initialize orders schema and seed records for execution plan analysis."""
    cursor = conn.cursor()
    cursor.executescript(
        """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            total_amount REAL NOT NULL,
            order_date TEXT NOT NULL
        );
        """
    )

    # Seed 1,000 synthetic order rows to ensure optimizer uses index heuristics
    records = []
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    for i in range(1, 1001):
        cust_id = (i % 50) + 1
        st = statuses[i % len(statuses)]
        amount = round(50.0 + (i * 0.75) % 450.0, 2)
        month = str((i % 12) + 1).zfill(2)
        date_str = f"2026-{month}-15"
        records.append((cust_id, st, amount, date_str))

    cursor.executemany(
        """
        INSERT INTO orders (customer_id, status, total_amount, order_date)
        VALUES (?, ?, ?, ?);
        """,
        records,
    )
    conn.commit()


def explain_query_plan(
    conn: sqlite3.Connection,
    query: str,
    params: Tuple[Any, ...] = (),
) -> List[str]:
    """Execute EXPLAIN QUERY PLAN and return human-readable plan steps."""
    cursor = conn.cursor()
    cursor.execute(f"EXPLAIN QUERY PLAN {query}", params)
    # SQLite returns (id, parent, notused, detail)
    return [row[3] for row in cursor.fetchall()]


def benchmark_single_column_index(conn: sqlite3.Connection) -> Dict[str, str]:
    """Compare query plan before and after single-column B-Tree index creation."""
    query = "SELECT * FROM orders WHERE total_amount > 400.0;"
    
    # Plan before index
    plan_before = " | ".join(explain_query_plan(conn, query))

    # Create index
    conn.execute("CREATE INDEX idx_orders_total_amount ON orders(total_amount);")

    # Plan after index
    plan_after = " | ".join(explain_query_plan(conn, query))

    return {
        "query": query,
        "plan_before_index": plan_before,
        "plan_after_index": plan_after,
    }


def demonstrate_composite_prefix_rule(conn: sqlite3.Connection) -> Dict[str, Any]:
    """Demonstrate Leftmost Prefix Rule on composite index (customer_id, status)."""
    conn.execute("CREATE INDEX idx_orders_cust_status ON orders(customer_id, status);")

    # Query A: filters on both columns (optimal index search)
    query_a = "SELECT * FROM orders WHERE customer_id = 42 AND status = 'shipped';"
    plan_a = " | ".join(explain_query_plan(conn, query_a))

    # Query B: filters on leftmost prefix (customer_id only - uses index)
    query_b = "SELECT * FROM orders WHERE customer_id = 42;"
    plan_b = " | ".join(explain_query_plan(conn, query_b))

    # Query C: filters on non-prefix column (status only - full scan)
    query_c = "SELECT * FROM orders WHERE status = 'shipped';"
    plan_c = " | ".join(explain_query_plan(conn, query_c))

    return {
        "composite_index": "idx_orders_cust_status ON orders(customer_id, status)",
        "query_prefix_and_second": {"query": query_a, "plan": plan_a},
        "query_prefix_only": {"query": query_b, "plan": plan_b},
        "query_non_prefix_only": {"query": query_c, "plan": plan_c},
    }


def demonstrate_sargability(conn: sqlite3.Connection) -> Dict[str, Any]:
    """Compare non-sargable function wrap vs sargable range query on indexed column."""
    conn.execute("CREATE INDEX idx_orders_date ON orders(order_date);")

    # Non-sargable: column wrapped in function
    non_sargable_query = "SELECT * FROM orders WHERE SUBSTR(order_date, 1, 7) = '2026-05';"
    non_sargable_plan = " | ".join(explain_query_plan(conn, non_sargable_query))

    # Sargable: direct column range bounds
    sargable_query = "SELECT * FROM orders WHERE order_date >= '2026-05-01' AND order_date < '2026-06-01';"
    sargable_plan = " | ".join(explain_query_plan(conn, sargable_query))

    return {
        "non_sargable": {"query": non_sargable_query, "plan": non_sargable_plan},
        "sargable": {"query": sargable_query, "plan": sargable_plan},
    }
