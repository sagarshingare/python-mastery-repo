"""Asyncio event loop management and advanced patterns.

This module demonstrates event loop management, including:
- Running async code in different contexts
- Event loop lifecycle management
- Integration with synchronous code
- Custom event loop policies

Python version: 3.10+
"""

from __future__ import annotations

import asyncio
import threading
import time
from typing import Any


async def simple_async_operation(value: int) -> int:
    """Simple async operation for demonstration.

    Args:
        value: Input value.

    Returns:
        Processed value.

    Example:
        await simple_async_operation(5) -> 10
    """
    await asyncio.sleep(0.1)
    return value * 2


def run_async_in_thread() -> int:
    """Run async code in a separate thread with its own event loop.

    Returns:
        Result from the async operation.

    Example:
        run_async_in_thread() -> 20
    """
    async def main() -> int:
        return await simple_async_operation(10)

    # Create new event loop for this thread
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(main())
    finally:
        loop.close()


async def run_sync_function_in_executor(func: callable, *args: Any) -> Any:
    """Run a synchronous function in a thread executor.

    Args:
        func: The synchronous function to run.
        *args: Arguments for the function.

    Returns:
        Result from the synchronous function.

    Example:
        await run_sync_function_in_executor(time.sleep, 0.1) -> None
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args)


async def demonstrate_executor_usage() -> dict[str, Any]:
    """Demonstrate running blocking operations in executors.

    Returns:
        Dictionary with timing information.

    Example:
        await demonstrate_executor_usage() -> {"sync_duration": 0.2, "async_duration": 0.1}
    """
    start_time = time.time()

    # Run blocking sleep in executor
    await run_sync_function_in_executor(time.sleep, 0.2)

    sync_duration = time.time() - start_time
    start_time = time.time()

    # Run async sleep
    await asyncio.sleep(0.1)

    async_duration = time.time() - start_time

    return {
        "sync_duration": round(sync_duration, 2),
        "async_duration": round(async_duration, 2)
    }


async def create_task_and_monitor() -> dict[str, Any]:
    """Create a task and monitor its lifecycle.

    Returns:
        Dictionary with task execution details.

    Example:
        await create_task_and_monitor() -> {"task_done": True, "result": 42}
    """
    async def background_task() -> int:
        await asyncio.sleep(0.2)
        return 42

    task = asyncio.create_task(background_task())

    # Monitor task
    while not task.done():
        await asyncio.sleep(0.05)
        print(f"Task running... done={task.done()}")

    result = await task
    return {"task_done": task.done(), "result": result}


class EventLoopManager:
    """Context manager for event loop lifecycle management."""

    def __init__(self) -> None:
        self.loop: asyncio.AbstractEventLoop | None = None

    async def __aenter__(self) -> 'EventLoopManager':
        self.loop = asyncio.get_running_loop()
        print("Entered event loop context")
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        print("Exiting event loop context")
        # Perform any cleanup here
        pass

    async def run_operation(self, operation: callable) -> Any:
        """Run an async operation within the managed context.

        Args:
            operation: Async callable to run.

        Returns:
            Result from the operation.
        """
        if self.loop is None:
            raise RuntimeError("Not in event loop context")
        return await operation()


async def demonstrate_loop_manager() -> str:
    """Demonstrate event loop context management.

    Returns:
        Success message.

    Example:
        await demonstrate_loop_manager() -> "Loop management completed"
    """
    async with EventLoopManager() as manager:
        result = await manager.run_operation(simple_async_operation(5))
        print(f"Operation result: {result}")

    return "Loop management completed"


def run_async_from_sync() -> int:
    """Run async code from synchronous context.

    Returns:
        Result from async operation.

    Example:
        run_async_from_sync() -> 30
    """
    async def async_main() -> int:
        return await simple_async_operation(15)

    return asyncio.run(async_main())