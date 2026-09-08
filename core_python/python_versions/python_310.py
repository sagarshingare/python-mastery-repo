"""
Python 3.10 Landmark Features & Idioms
=====================================
Released: October 2021

Key Features:
1. PEP 634-636: Structural Pattern Matching (`match / case`)
2. PEP 604: New Type Union Operator (`X | Y` syntax)
3. PEP 618: `zip(..., strict=True)` for length verification
4. Parenthesized Multi-line Context Managers
5. PEP 612: `typing.ParamSpec` and `typing.Concatenate`
6. PEP 613: Explicit Type Aliases (`TypeAlias`)
"""

from __future__ import annotations
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union

T = TypeVar("T")


# --- 1. Structural Pattern Matching (PEP 634) ---
# Note: Full match/case AST is evaluated dynamically on Python 3.10+
PATTERN_MATCHING_CODE = """
def evaluate_event(event: dict) -> str:
    match event:
        case {"type": "click", "x": int(x), "y": int(y)}:
            return f"Clicked at coordinates ({x}, {y})"
        case {"type": "keypress", "key": "Enter" | "Return"}:
            return "Submit action triggered"
        case {"type": "keypress", "key": str(key)}:
            return f"Key pressed: {key}"
        case {"type": "error", "code": int(code)} if code >= 500:
            return f"Server error: {code}"
        case {"type": "error", "code": int(code)}:
            return f"Client/Request error: {code}"
        case [command, *args]:
            return f"CLI command: {command} with args: {args}"
        case _:
            return "Unknown event"
"""

if sys.version_info >= (3, 10):
    _local_scope: Dict[str, Any] = {}
    exec(PATTERN_MATCHING_CODE, globals(), _local_scope)
    evaluate_event = _local_scope["evaluate_event"]
else:
    def evaluate_event(event: Any) -> str:
        """Fallback pattern matching dispatcher for Python < 3.10."""
        if isinstance(event, dict):
            event_type = event.get("type")
            if event_type == "click" and isinstance(event.get("x"), int) and isinstance(event.get("y"), int):
                return f"Clicked at coordinates ({event['x']}, {event['y']})"
            elif event_type == "keypress" and event.get("key") in ("Enter", "Return"):
                return "Submit action triggered"
            elif event_type == "keypress" and isinstance(event.get("key"), str):
                return f"Key pressed: {event['key']}"
            elif event_type == "error" and isinstance(event.get("code"), int):
                code = event["code"]
                if code >= 500:
                    return f"Server error: {code}"
                return f"Client/Request error: {code}"
        elif isinstance(event, list) and len(event) > 0:
            return f"CLI command: {event[0]} with args: {event[1:]}"
        return "Unknown event"


# --- 2. Strict Zip (PEP 618) ---
def safe_zip(seq_a: list[Any], seq_b: list[Any]) -> list[tuple[Any, Any]]:
    """Demonstrates zip(..., strict=True) to catch unequal iterable lengths."""
    if sys.version_info >= (3, 10):
        # Native zip(..., strict=True)
        return list(zip(seq_a, seq_b, strict=True))  # type: ignore
    else:
        # Fallback simulation
        if len(seq_a) != len(seq_b):
            raise ValueError(f"safe_zip: length mismatch ({len(seq_a)} != {len(seq_b)})")
        return list(zip(seq_a, seq_b))


# --- 3. Parenthesized Context Managers ---
# In Python 3.10+, you can cleanly wrap multiple context managers:
# with (
#     open("file1.txt") as f1,
#     open("file2.txt") as f2,
# ):
#     ...


# --- 4. Union Syntax & ParamSpec ---
# In Python 3.10+, type annotations support `int | str` directly instead of `Union[int, str]`.
def parse_response_status(status_code: Union[int, str]) -> str:
    """Type union representing flexible input."""
    code = int(status_code)
    if 200 <= code < 300:
        return "SUCCESS"
    elif 400 <= code < 500:
        return "CLIENT_ERROR"
    return "SERVER_ERROR"


def run_python_310_demos() -> None:
    """Execute all Python 3.10 feature demonstrations."""
    print("=== Python 3.10 Feature Demonstrations ===")

    # 1. Pattern Matching
    events = [
        {"type": "click", "x": 100, "y": 200},
        {"type": "keypress", "key": "Enter"},
        {"type": "error", "code": 503},
        {"type": "error", "code": 404},
        ["git", "commit", "-m", "update"],
        {"unknown": True},
    ]
    print(f"1. Structural Pattern Matching (Native: {sys.version_info >= (3, 10)}):")
    for ev in events:
        res = evaluate_event(ev)
        print(f"   Event {ev} -> {res}")

    # 2. Strict Zip
    keys = ["id", "username", "role"]
    vals = [101, "charlie", "admin"]
    paired = safe_zip(keys, vals)
    print(f"\n2. Safe strict zip paired: {paired}")

    try:
        safe_zip(["a", "b"], [1, 2, 3])
    except ValueError as err:
        print(f"   Expected ValueError on mismatched zip lengths: {err}")

    # 3. Union type
    print(f"\n3. Union type evaluation: {parse_response_status('200')}, {parse_response_status(404)}")

    print("Python 3.10 demonstrations completed successfully!\n")


if __name__ == "__main__":
    run_python_310_demos()
