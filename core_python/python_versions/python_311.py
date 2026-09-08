"""
Python 3.11 Landmark Features & Idioms
=====================================
Released: October 2022

Key Features:
1. PEP 654: Exception Groups (`ExceptionGroup`) & `except*` Syntax
2. PEP 678: Exception Notes (`err.add_note()`)
3. PEP 680: `tomllib` (Native Standard Library TOML Parser)
4. PEP 654 / asyncio: `asyncio.TaskGroup` for Structured Concurrency
5. PEP 673: `typing.Self` for Fluent Interface Method Chaining
6. PEP 657: Fine-grained Error Locations in Tracebacks
7. Faster CPython Project (Adaptive Specializing Interpreter: 10-60% faster)
"""

from __future__ import annotations
import sys
from typing import Any, Dict, List, Optional


# --- 1. Exception Notes (PEP 678) ---
def parse_record_with_notes(record: dict) -> int:
    """Demonstrates adding context notes to exceptions without rewrapping."""
    try:
        val = int(record["value"])
        if val < 0:
            raise ValueError("Value cannot be negative")
        return val
    except Exception as exc:
        if hasattr(exc, "add_note"):
            exc.add_note(f"Encountered while processing record ID: {record.get('id', 'unknown')}")
            exc.add_note(f"Record payload: {record}")
        raise


# --- 2. Exception Groups & except* (PEP 654) ---
EXCEPTION_GROUP_CODE = """
def trigger_exception_group():
    errors = [
        ValueError("Invalid format in chunk 1"),
        TypeError("Expected integer in chunk 2"),
        ConnectionResetError("Socket lost in chunk 3"),
    ]
    raise ExceptionGroup("Batch processing multi-failure", errors)

def handle_exception_group():
    try:
        trigger_exception_group()
    except* ValueError as eg:
        return f"Handled ValueErrors: {eg.exceptions}"
    except* TypeError as eg:
        return f"Handled TypeErrors: {eg.exceptions}"
    except* Exception as eg:
        return f"Handled remaining exceptions: {eg.exceptions}"
"""

if sys.version_info >= (3, 11):
    _local_eg_scope: Dict[str, Any] = {}
    exec(EXCEPTION_GROUP_CODE, globals(), _local_eg_scope)
    trigger_exception_group = _local_eg_scope["trigger_exception_group"]
    handle_exception_group = _local_eg_scope["handle_exception_group"]
else:
    def trigger_exception_group() -> None:
        """Emulated exception group for Python < 3.11."""
        raise RuntimeError("ExceptionGroup requires Python 3.11+ runtime")

    def handle_exception_group() -> str:
        return "ExceptionGroup / except* requires Python 3.11+ runtime"


# --- 3. tomllib Standard TOML Parsing (PEP 680) ---
def parse_toml_string(toml_data: str) -> dict:
    """Parses TOML using standard library tomllib (Python 3.11+) or fallback."""
    try:
        import tomllib
        return tomllib.loads(toml_data)
    except ImportError:
        # Minimal key=value fallback for demo on older Python
        result = {}
        for line in toml_data.strip().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                result[k.strip()] = v.strip().strip('"')
        return result


# --- 4. typing.Self Pattern (PEP 673) ---
class QueryBuilder:
    """Demonstrates method chaining using Self semantics."""

    def __init__(self) -> None:
        self.clauses: List[str] = []

    def select(self, columns: str) -> QueryBuilder:
        self.clauses.append(f"SELECT {columns}")
        return self

    def from_table(self, table: str) -> QueryBuilder:
        self.clauses.append(f"FROM {table}")
        return self

    def where(self, condition: str) -> QueryBuilder:
        self.clauses.append(f"WHERE {condition}")
        return self

    def build(self) -> str:
        return " ".join(self.clauses)


def run_python_311_demos() -> None:
    """Execute all Python 3.11 feature demonstrations."""
    print("=== Python 3.11 Feature Demonstrations ===")

    # 1. Exception Notes
    print(f"1. Exception Notes (Supported: {hasattr(BaseException, 'add_note')}):")
    bad_record = {"id": "rec_99", "value": "-50"}
    try:
        parse_record_with_notes(bad_record)
    except Exception as err:
        notes = getattr(err, "__notes__", None)
        print(f"   Caught error: {err}")
        if notes:
            print(f"   Attached notes: {notes}")
        else:
            print("   Notes not supported on this Python runtime.")

    # 2. Exception Groups
    print(f"\n2. Exception Groups & except* (Supported: {sys.version_info >= (3, 11)}):")
    print(f"   Handler result: {handle_exception_group()}")

    # 3. tomllib
    sample_toml = """
    title = "Python Mastery Config"
    version = "1.0.0"
    """
    parsed = parse_toml_string(sample_toml)
    print(f"\n3. TOML Config Parsed: {parsed}")

    # 4. Fluent Builder
    query = QueryBuilder().select("id, name").from_table("users").where("active = 1").build()
    print(f"\n4. QueryBuilder fluent chaining: {query}")

    print("Python 3.11 demonstrations completed successfully!\n")


if __name__ == "__main__":
    run_python_311_demos()
