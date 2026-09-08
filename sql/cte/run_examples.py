"""CLI runner for Common Table Expression (CTE) demonstrations."""

from __future__ import annotations

import argparse
import logging

from sql.cte.cte_operations import (
    create_connection,
    generate_number_sequence,
    get_modular_pipeline_cte,
    get_org_chart_hierarchy,
    init_cte_db,
)

logger = logging.getLogger(__name__)


def run_modular_demo() -> None:
    logger.info("Running CTE: Modular Multi-Stage Pipeline")
    conn = create_connection()
    try:
        init_cte_db(conn)
        orders = get_modular_pipeline_cte(conn)
        print("Orders from above-average regions (via multi-stage CTE):")
        for o in orders:
            print(f"  - Order #{o['order_id']}: {o['customer_name']} (${o['amount']:,.2f}) [{o['region']} Total: ${o['region_total']:,.2f}]")
    finally:
        conn.close()


def run_sequence_demo() -> None:
    logger.info("Running CTE: Recursive Number Sequence Generation")
    conn = create_connection()
    try:
        seq = generate_number_sequence(conn, start=1, end=10)
        print(f"Generated sequence [1..10]: {seq}")
    finally:
        conn.close()


def run_hierarchy_demo() -> None:
    logger.info("Running CTE: Recursive Tree Traversal (Org Chart)")
    conn = create_connection()
    try:
        init_cte_db(conn)
        org = get_org_chart_hierarchy(conn)
        print("Organizational Hierarchy Tree Traversal:")
        for emp in org:
            indent = "  " * emp['depth']
            print(f"{indent}L{emp['depth']} - {emp['name']} ({emp['title']})")
            print(f"{indent}     Path: {emp['management_path']}")
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="SQL CTE Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["modular", "sequence", "hierarchy", "all"],
        default="all",
        help="Demonstration to run (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "modular": run_modular_demo,
        "sequence": run_sequence_demo,
        "hierarchy": run_hierarchy_demo,
    }

    if args.demo == "all":
        for fn in dispatch.values():
            fn()
            print()
    else:
        dispatch[args.demo]()


if __name__ == "__main__":
    main()
