"""CLI runner for SQL Fundamentals demonstrations."""

from __future__ import annotations

import argparse
import logging

from sql.basics.fundamentals import (
    batch_insert_employees,
    create_connection,
    delete_inactive_employees,
    filter_employees,
    get_department_metrics,
    init_fundamentals_db,
    insert_employee,
    paginate_employees,
    update_employee_salary,
)

logger = logging.getLogger(__name__)


def run_crud_demo() -> None:
    logger.info("Running SQL Fundamentals: CRUD operations")
    conn = create_connection()
    try:
        init_fundamentals_db(conn)
        new_id = insert_employee(
            conn,
            first_name="Barbara",
            last_name="Liskov",
            email="barbara@example.com",
            department_id=1,
            salary=145000.0,
            hire_date="2024-01-01",
        )
        print(f"Inserted new employee ID: {new_id}")

        updated = update_employee_salary(conn, department_id=1, multiplier=1.05)
        print(f"Updated {updated} employees with 5% raise in Department 1")

        deleted = delete_inactive_employees(conn, hire_date_before="2024-01-01")
        print(f"Deleted {deleted} legacy inactive employee records")
    finally:
        conn.close()


def run_filtering_demo() -> None:
    logger.info("Running SQL Fundamentals: Dynamic Filtering")
    conn = create_connection()
    try:
        init_fundamentals_db(conn)
        filtered = filter_employees(
            conn,
            department_ids=[1, 2],
            min_salary=130000.0,
            email_domain="example.com",
        )
        print(f"Filtered {len(filtered)} active employees with salary >= 130k in Depts [1, 2]:")
        for emp in filtered:
            print(f"  - {emp['first_name']} {emp['last_name']} (${emp['salary']:,.2f}) [{emp['email']}]")
    finally:
        conn.close()


def run_aggregation_demo() -> None:
    logger.info("Running SQL Fundamentals: Aggregation and Grouping")
    conn = create_connection()
    try:
        init_fundamentals_db(conn)
        metrics = get_department_metrics(conn, min_headcount=1)
        print("Department Aggregations (HAVING headcount >= 1):")
        for m in metrics:
            print(
                f"  - {m['department_name']}: Headcount={m['employee_count']}, "
                f"Avg=${m['avg_salary']:,.2f}, Min=${m['min_salary']:,.2f}, Max=${m['max_salary']:,.2f}"
            )
    finally:
        conn.close()


def run_pagination_demo() -> None:
    logger.info("Running SQL Fundamentals: Offset Pagination")
    conn = create_connection()
    try:
        init_fundamentals_db(conn)
        total, page_1 = paginate_employees(conn, page=1, page_size=2)
        print(f"Page 1 (Total active employees: {total}):")
        for r in page_1:
            print(f"  #{r['id']} {r['full_name']} - ${r['salary']:,.2f}")

        _, page_2 = paginate_employees(conn, page=2, page_size=2)
        print("Page 2:")
        for r in page_2:
            print(f"  #{r['id']} {r['full_name']} - ${r['salary']:,.2f}")
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="SQL Fundamentals Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["crud", "filtering", "aggregation", "pagination", "all"],
        default="all",
        help="Demonstration to run (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "crud": run_crud_demo,
        "filtering": run_filtering_demo,
        "aggregation": run_aggregation_demo,
        "pagination": run_pagination_demo,
    }

    if args.demo == "all":
        for fn in dispatch.values():
            fn()
            print()
    else:
        dispatch[args.demo]()


if __name__ == "__main__":
    main()
