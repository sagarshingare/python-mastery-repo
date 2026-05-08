"""Asyncio task management and concurrent execution patterns.

This module demonstrates advanced asyncio task patterns, including:
- Creating and managing asyncio Tasks
- Task cancellation and exception handling
- Concurrent task execution with gather and wait
- Task lifecycle management

Python version: 3.10+
"""

from __future__ import annotations

import asyncio
import random
from typing import Any


async def simulate_work(task_id: int, duration: float) -> dict[str, Any]:
    """Simulate asynchronous work with variable duration.

    Args:
        task_id: Unique identifier for the task.
        duration: Time in seconds to simulate work.

    Returns:
        Dictionary containing task results.

    Example:
        await simulate_work(1, 0.5) -> {"task_id": 1, "result": "completed", "duration": 0.5}
    """
    await asyncio.sleep(duration)
    return {
        "task_id": task_id,
        "result": "completed",
        "duration": duration,
        "timestamp": asyncio.get_event_loop().time()
    }


async def create_and_run_tasks() -> list[dict[str, Any]]:
    """Create multiple tasks and run them concurrently.

    Returns:
        List of task results.

    Example:
        await create_and_run_tasks() -> [{"task_id": 1, ...}, {"task_id": 2, ...}, ...]
    """
    # Create tasks with different durations
    tasks = [
        asyncio.create_task(simulate_work(1, 0.1)),
        asyncio.create_task(simulate_work(2, 0.2)),
        asyncio.create_task(simulate_work(3, 0.15))
    ]

    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    return results


async def run_with_timeout() -> list[dict[str, Any]]:
    """Run tasks with a timeout to prevent hanging.

    Returns:
        List of completed task results.

    Example:
        await run_with_timeout() -> [{"task_id": 1, ...}, {"task_id": 2, ...}]
    """
    async def long_running_task(task_id: int) -> dict[str, Any]:
        # Random duration between 0.1 and 0.5 seconds
        duration = random.uniform(0.1, 0.5)
        await asyncio.sleep(duration)
        return {"task_id": task_id, "duration": duration}

    tasks = [long_running_task(i) for i in range(1, 4)]

    try:
        # Timeout after 0.3 seconds
        results = await asyncio.wait_for(asyncio.gather(*tasks), timeout=0.3)
        return results
    except asyncio.TimeoutError:
        return [{"error": "timeout", "completed_tasks": "partial"}]


async def handle_task_exceptions() -> list[dict[str, Any]]:
    """Demonstrate handling exceptions in concurrent tasks.

    Returns:
        List of results, including error information.

    Example:
        await handle_task_exceptions() -> [{"task_id": 1, "result": "success"}, {"task_id": 2, "error": "ValueError"}]
    """
    async def task_with_potential_error(task_id: int) -> dict[str, Any]:
        if task_id == 2:
            raise ValueError(f"Task {task_id} failed")
        await asyncio.sleep(0.1)
        return {"task_id": task_id, "result": "success"}

    tasks = [task_with_potential_error(i) for i in range(1, 4)]

    results = []
    for coro in tasks:
        try:
            result = await coro
            results.append(result)
        except ValueError as e:
            results.append({"task_id": "unknown", "error": str(e)})

    return results


async def cancel_running_tasks() -> dict[str, Any]:
    """Demonstrate task cancellation.

    Returns:
        Dictionary showing cancellation results.

    Example:
        await cancel_running_tasks() -> {"cancelled": True, "reason": "timeout"}
    """
    async def long_task() -> str:
        await asyncio.sleep(1.0)
        return "completed"

    task = asyncio.create_task(long_task())

    try:
        # Cancel after 0.2 seconds
        result = await asyncio.wait_for(task, timeout=0.2)
        return {"result": result}
    except asyncio.TimeoutError:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            return {"cancelled": True, "reason": "timeout"}