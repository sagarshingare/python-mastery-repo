"""CLI runner for SQL Join demonstrations."""

from __future__ import annotations

import argparse
import logging

from sql.joins.join_operations import (
    create_connection,
    get_anti_join_departments,
    get_cross_join_combinations,
    get_full_outer_join_simulation,
    get_inner_join_records,
    get_left_join_records,
    get_self_join_hierarchy,
    init_joins_db,
)

logger = logging.getLogger(__name__)


def run_inner_demo() -> None:
    logger.info("Running SQL Joins: INNER JOIN")
    conn = create_connection()
    try:
        init_joins_db(conn)
        records = get_inner_join_records(conn)
        print("INNER JOIN (Employees with valid departments):")
        for r in records:
            print(f"  - {r['employee_name']} works in {r['department_name']} (${r['salary']:,.2f})")
    finally:
        conn.close()


def run_left_demo() -> None:
    logger.info("Running SQL Joins: LEFT OUTER JOIN")
    conn = create_connection()
    try:
        init_joins_db(conn)
        records = get_left_join_records(conn)
        print("LEFT JOIN (All employees, handling unassigned departments):")
        for r in records:
            print(f"  - {r['employee_name']} -> Department: {r['department_name']}")
    finally:
        conn.close()


def run_anti_demo() -> None:
    logger.info("Running SQL Joins: ANTI-JOIN")
    conn = create_connection()
    try:
        init_joins_db(conn)
        records = get_anti_join_departments(conn)
        print("ANTI-JOIN (Departments with ZERO assigned employees):")
        for r in records:
            print(f"  - Dept #{r['department_id']}: {r['department_name']}")
    finally:
        conn.close()


def run_self_demo() -> None:
    logger.info("Running SQL Joins: SELF JOIN")
    conn = create_connection()
    try:
        init_joins_db(conn)
        records = get_self_join_hierarchy(conn)
        print("SELF JOIN (Employee reporting hierarchy):")
        for r in records:
            print(f"  - {r['employee_name']} reports to -> {r['manager_name']}")
    finally:
        conn.close()


def run_cross_demo() -> None:
    logger.info("Running SQL Joins: CROSS JOIN")
    conn = create_connection()
    try:
        init_joins_db(conn)
        records = get_cross_join_combinations(conn)
        print("CROSS JOIN (Product size matrix / Cartesian product):")
        for r in records:
            print(f"  - SKU: {r['sku']} ({r['product_code']} in {r['size_name']})")
    finally:
        conn.close()


def run_full_demo() -> None:
    logger.info("Running SQL Joins: FULL OUTER JOIN simulation")
    conn = create_connection()
    try:
        init_joins_db(conn)
        records = get_full_outer_join_simulation(conn)
        print("FULL OUTER JOIN (via UNION):")
        for r in records:
            emp = r['employee_name'] or "None"
            dept = r['department_name'] or "None"
            print(f"  - Employee: {emp.ljust(18)} | Dept: {dept}")
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="SQL Join Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["inner", "left", "anti", "self", "cross", "full", "all"],
        default="all",
        help="Demonstration to run (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "inner": run_inner_demo,
        "left": run_left_demo,
        "anti": run_anti_demo,
        "self": run_self_demo,
        "cross": run_cross_demo,
        "full": run_full_demo,
    }

    if args.demo == "all":
        for fn in dispatch.values():
            fn()
            print()
    else:
        dispatch[args.demo]()


if __name__ == "__main__":
    main()
