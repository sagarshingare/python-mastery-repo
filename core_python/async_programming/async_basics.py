"""Asynchronous programming basics in Python.

This module demonstrates fundamental async/await patterns, including:
- Defining and calling async functions
- Using await for asynchronous operations
- Basic asyncio event loop management
- Handling async context and cleanup

Python version: 3.10+
"""

from __future__ import annotations

import asyncio
import time
from typing import Any


async def async_delayed_greeting(name: str, delay: float = 1.0) -> str:
    """Return a greeting after an asynchronous delay.

    Args:
        name: The name to greet.
        delay: Seconds to wait before returning the greeting.

    Returns:
        A formatted greeting string.

    Example:
        await async_delayed_greeting("Alice", 0.5) -> "Hello, Alice!"
    """
    await asyncio.sleep(delay)
    return f"Hello, {name}!"


async def async_calculate_sum(numbers: list[int]) -> int:
    """Asynchronously calculate the sum of a list of numbers.

    This simulates an async operation that might involve I/O.

    Args:
        numbers: List of integers to sum.

    Returns:
        The sum of all numbers.

    Example:
        await async_calculate_sum([1, 2, 3, 4]) -> 10
    """
    # Simulate async work
    await asyncio.sleep(0.1)
    return sum(numbers)


async def async_fetch_data(source: str) -> dict[str, Any]:
    """Simulate fetching data from an async source.

    Args:
        source: The data source identifier.

    Returns:
        A dictionary containing fetched data.

    Example:
        await async_fetch_data("api") -> {"status": "success", "data": [1, 2, 3]}
    """
    await asyncio.sleep(0.2)  # Simulate network delay
    return {
        "status": "success",
        "source": source,
        "data": [1, 2, 3, 4, 5],
        "timestamp": time.time()
    }


async def run_sequential_operations() -> list[str]:
    """Run multiple async operations sequentially.

    Returns:
        List of results from each operation.

    Example:
        await run_sequential_operations() -> ["Hello, Alice!", "Hello, Bob!", "Hello, Charlie!"]
    """
    names = ["Alice", "Bob", "Charlie"]
    results = []

    for name in names:
        result = await async_delayed_greeting(name, 0.1)
        results.append(result)

    return results


async def run_concurrent_operations() -> list[str]:
    """Run multiple async operations concurrently using asyncio.gather.

    Returns:
        List of results from each operation.

    Example:
        await run_concurrent_operations() -> ["Hello, Alice!", "Hello, Bob!", "Hello, Charlie!"]
    """
    names = ["Alice", "Bob", "Charlie"]
    tasks = [async_delayed_greeting(name, 0.1) for name in names]
    return await asyncio.gather(*tasks)