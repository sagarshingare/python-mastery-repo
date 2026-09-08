"""
Python 3.9 Landmark Features & Idioms
====================================
Released: October 2020

Key Features:
1. PEP 584: Dictionary Merge (`|`) and Update (`|=`) Operators
2. PEP 616: String Prefix & Suffix Stripping (`removeprefix` / `removesuffix`)
3. PEP 585: Type Hinting Generics in Standard Collections (`list[int]`, `dict[str, Any]`)
4. PEP 615: The `zoneinfo` Module (Standard IANA Time Zone Support)
5. `graphlib.TopologicalSorter`: Dependency Resolution & DAG Ordering
"""

from __future__ import annotations
import graphlib
from typing import Any, Dict, List
import zoneinfo


# --- 1. Dict Merge (|) and Update (|=) Operators (PEP 584) ---
def merge_configs(default_config: dict[str, Any], user_config: dict[str, Any]) -> dict[str, Any]:
    """Merge dictionary with pipe operator (|).

    Unlike {**d1, **d2}, this respects dict subclasses and is cleaner.
    """
    return default_config | user_config


def update_in_place(target_dict: dict[str, Any], overrides: dict[str, Any]) -> None:
    """In-place dictionary update using (|=)."""
    target_dict |= overrides


# --- 2. String Methods: removeprefix & removesuffix (PEP 616) ---
def sanitize_identifier(raw_identifier: str) -> str:
    """Demonstrates removeprefix and removesuffix.

    Crucial distinction vs str.lstrip/rstrip:
    - lstrip('prefix_') strips any character set {'p','r','e','f','i','x','_'} repeatedly!
    - removeprefix('prefix_') removes the exact prefix sequence once.
    """
    cleaned = raw_identifier.removeprefix("tbl_").removesuffix("_temp")
    return cleaned


# --- 3. PEP 585 Standard Collection Generics ---
# Note: list[str], dict[str, int] can now be written without importing List, Dict from typing.
def aggregate_scores(records: list[dict[str, int]]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for r in records:
        for key, val in r.items():
            totals[key] = totals.get(key, 0) + val
    return totals


# --- 4. graphlib.TopologicalSorter: DAG Scheduling ---
def resolve_build_dependencies(task_graph: dict[str, set[str]]) -> list[str]:
    """Order tasks such that all dependencies are resolved first."""
    sorter = graphlib.TopologicalSorter(task_graph)
    return list(sorter.static_order())


# --- 5. zoneinfo Standard Timezones (PEP 615) ---
def get_timezone_info(tz_name: str = "UTC") -> str:
    """Create IANA timezone using standard library zoneinfo (replaces pytz)."""
    from datetime import datetime
    try:
        tz = zoneinfo.ZoneInfo(tz_name)
        now = datetime.now(tz)
        return f"Time in {tz_name}: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except Exception as err:
        return f"ZoneInfo unavailable for {tz_name}: {err}"


def run_python_39_demos() -> None:
    """Execute all Python 3.9 feature demonstrations."""
    print("=== Python 3.9 Feature Demonstrations ===")

    # 1. Dict Merge & Update
    base = {"theme": "light", "timeout": 30, "retries": 3}
    override = {"theme": "dark", "retries": 5}
    merged = merge_configs(base, override)
    print(f"1. Dict merge (|): {merged}")
    assert merged["theme"] == "dark" and merged["timeout"] == 30

    in_place = {"a": 1}
    update_in_place(in_place, {"b": 2, "a": 10})
    print(f"   Dict update in-place (|=): {in_place}")

    # 2. removeprefix / removesuffix
    raw_name = "tbl_customer_orders_temp"
    cleaned = sanitize_identifier(raw_name)
    print(f"2. removeprefix/suffix: '{raw_name}' -> '{cleaned}'")
    assert cleaned == "customer_orders"

    # 3. Builtin Generics
    scores = [{"math": 90, "algo": 95}, {"math": 85, "sys": 92}]
    agg = aggregate_scores(scores)
    print(f"3. PEP 585 Generics aggregation: {agg}")

    # 4. Topological Sort
    pipeline = {
        "deploy": {"build", "test"},
        "test": {"compile"},
        "build": {"compile"},
        "compile": set(),
    }
    execution_order = resolve_build_dependencies(pipeline)
    print(f"4. Topological build order: {execution_order}")
    assert execution_order.index("compile") < execution_order.index("test")
    assert execution_order.index("test") < execution_order.index("deploy")

    # 5. ZoneInfo
    print(f"5. ZoneInfo: {get_timezone_info('UTC')}")

    print("Python 3.9 demonstrations completed successfully!\n")


if __name__ == "__main__":
    run_python_39_demos()
