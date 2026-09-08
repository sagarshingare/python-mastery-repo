"""
Python 3.8 Landmark Features & Idioms
====================================
Released: October 2019

Key Features:
1. PEP 572: Assignment Expressions (The Walrus Operator `:=`)
2. PEP 570: Positional-Only Parameters (`/` syntax)
3. f-string debugging syntax (`f"{expr=}"`)
4. New math functions: `math.prod()`, `math.isqrt()`
5. Typing additions: `TypedDict`, `Literal`, `Final`, `Protocol`
"""

from __future__ import annotations
import math
import re
from typing import Final, List, Literal, Optional, TypedDict


# --- 1. Positional-Only Parameters (PEP 570) ---
def compute_discount(price: float, discount_rate: float, /, currency: str = "USD", *, tax: float = 0.0) -> float:
    """Demonstrates positional-only (`/`) and keyword-only (`*`) parameters.

    - `price` and `discount_rate` MUST be passed positionally.
    - `currency` can be passed positionally or as keyword.
    - `tax` MUST be passed as keyword.
    """
    discounted = price * (1.0 - discount_rate)
    return round(discounted * (1.0 + tax), 2)


# --- 2. Typing Additions: TypedDict, Literal, Final ---
Environment = Literal["development", "staging", "production"]
MAX_RETRIES: Final[int] = 3


class ServerConfig(TypedDict):
    host: str
    port: int
    env: Environment
    debug: bool


def configure_server(config: ServerConfig) -> str:
    return f"Starting server on {config['host']}:{config['port']} (env: {config['env']})"


# --- 3. Walrus Operator (PEP 572) ---
def filter_and_transform_data(raw_items: List[str]) -> List[dict]:
    """Demonstrates walrus `:=` in filtering conditions and comprehensions."""
    # Walrus in comprehension: compute length once, test condition and store
    results = [
        {"item": item, "length": n}
        for item in raw_items
        if (n := len(item.strip())) >= 4
    ]
    return results


def parse_query_params(query: str) -> dict:
    """Demonstrates walrus `:=` in regex matching."""
    params = {}
    pattern = re.compile(r"(\w+)=([^&]+)")
    pos = 0
    # Walrus in while loop
    while match := pattern.search(query, pos):
        key, val = match.groups()
        params[key] = val
        pos = match.end()
    return params


# --- 4. Math Additions: math.prod & math.isqrt ---
def calculate_metrics(factors: List[int], large_number: int) -> tuple[int, int]:
    """Demonstrates math.prod and exact integer square root math.isqrt."""
    product = math.prod(factors)
    exact_root = math.isqrt(large_number)
    return product, exact_root


def run_python_38_demos() -> None:
    """Execute all Python 3.8 feature demonstrations."""
    print("=== Python 3.8 Feature Demonstrations ===")

    # 1. Positional-only params
    total = compute_discount(100.0, 0.20, "USD", tax=0.05)
    print(f"1. Positional-only result: {total}")
    try:
        # Calling positional-only argument as keyword raises TypeError
        compute_discount(price=100.0, discount_rate=0.20)  # type: ignore
    except TypeError as err:
        print(f"   Expected TypeError on keyword call: {err}")

    # 2. Walrus operator
    items = ["py", "python", "mastery", "go", "rust"]
    filtered = filter_and_transform_data(items)
    print(f"2. Walrus filtered items (length >= 4): {filtered}")

    params = parse_query_params("user=alice&role=admin&active=true")
    print(f"   Walrus parsed query params: {params}")

    # 3. f-string debugging specifier
    x = 42
    y = 58
    print(f"3. f-string debugging: {x=}, {y=}, {x + y=}")

    # 4. Math enhancements
    factors = [2, 3, 4, 5]
    product, root = calculate_metrics(factors, 144)
    print(f"4. math.prod({factors})={product}, math.isqrt(144)={root}")

    # 5. TypedDict and Literal
    config: ServerConfig = {"host": "0.0.0.0", "port": 8000, "env": "production", "debug": False}
    print(f"5. TypedDict config: {configure_server(config)}")

    print("Python 3.8 demonstrations completed successfully!\n")


if __name__ == "__main__":
    run_python_38_demos()
