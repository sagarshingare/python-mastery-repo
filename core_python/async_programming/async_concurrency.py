"""Concurrent execution patterns with asyncio.

This module demonstrates concurrent programming patterns, including:
- Producer-consumer patterns
- Semaphore-based resource limiting
- Concurrent data processing
- Async context managers for resource management

Python version: 3.10+
"""

from __future__ import annotations

import asyncio
import random
from typing import Any


async def producer_consumer_pattern() -> dict[str, Any]:
    """Demonstrate producer-consumer pattern with asyncio.Queue.

    Returns:
        Dictionary containing production and consumption statistics.

    Example:
        await producer_consumer_pattern() -> {"produced": 10, "consumed": 10, "total_processed": 10}
    """
    queue = asyncio.Queue()
    produced = 0
    consumed = 0

    async def producer() -> None:
        nonlocal produced
        for i in range(10):
            item = f"item_{i}"
            await queue.put(item)
            produced += 1
            await asyncio.sleep(random.uniform(0.01, 0.05))

    async def consumer(consumer_id: int) -> None:
        nonlocal consumed
        while True:
            try:
                item = await asyncio.wait_for(queue.get(), timeout=0.1)
                consumed += 1
                # Process item
                await asyncio.sleep(random.uniform(0.02, 0.08))
                queue.task_done()
            except asyncio.TimeoutError:
                break

    # Start producer and multiple consumers
    producer_task = asyncio.create_task(producer())
    consumer_tasks = [asyncio.create_task(consumer(i)) for i in range(3)]

    await producer_task
    await queue.join()  # Wait for all items to be processed

    # Cancel consumers
    for task in consumer_tasks:
        task.cancel()
    await asyncio.gather(*consumer_tasks, return_exceptions=True)

    return {
        "produced": produced,
        "consumed": consumed,
        "total_processed": produced
    }


async def semaphore_limited_concurrency() -> list[int]:
    """Use semaphore to limit concurrent operations.

    Returns:
        List of results from concurrent operations.

    Example:
        await semaphore_limited_concurrency() -> [0, 1, 2, 3, 4]
    """
    semaphore = asyncio.Semaphore(3)  # Limit to 3 concurrent operations

    async def limited_operation(value: int) -> int:
        async with semaphore:
            await asyncio.sleep(0.1)  # Simulate work
            return value * 2

    # Create more tasks than semaphore limit
    tasks = [limited_operation(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    return sorted(results)


async def concurrent_data_processing(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Process data concurrently with error handling.

    Args:
        data: List of data items to process.

    Returns:
        List of processed results.

    Example:
        data = [{"id": 1, "value": 10}, {"id": 2, "value": 20}]
        await concurrent_data_processing(data) -> [{"id": 1, "processed": 20}, {"id": 2, "processed": 40}]
    """
    async def process_item(item: dict[str, Any]) -> dict[str, Any]:
        try:
            # Simulate processing time
            await asyncio.sleep(random.uniform(0.05, 0.15))
            return {
                "id": item["id"],
                "processed": item["value"] * 2,
                "status": "success"
            }
        except Exception as e:
            return {
                "id": item.get("id", "unknown"),
                "error": str(e),
                "status": "failed"
            }

    tasks = [process_item(item) for item in data]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle any exceptions that occurred
    processed_results = []
    for result in results:
        if isinstance(result, Exception):
            processed_results.append({"error": str(result), "status": "exception"})
        else:
            processed_results.append(result)

    return processed_results


class AsyncResourceManager:
    """Async context manager for resource management."""

    def __init__(self, resource_id: str) -> None:
        self.resource_id = resource_id
        self.acquired = False

    async def __aenter__(self) -> 'AsyncResourceManager':
        print(f"Acquiring resource {self.resource_id}")
        await asyncio.sleep(0.05)  # Simulate acquisition time
        self.acquired = True
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        print(f"Releasing resource {self.resource_id}")
        await asyncio.sleep(0.05)  # Simulate cleanup time
        self.acquired = False

    async def use_resource(self) -> str:
        """Use the acquired resource."""
        if not self.acquired:
            raise RuntimeError("Resource not acquired")
        await asyncio.sleep(0.1)  # Simulate usage
        return f"Used resource {self.resource_id}"


async def demonstrate_resource_manager() -> list[str]:
    """Demonstrate async context manager usage.

    Returns:
        List of resource usage results.

    Example:
        await demonstrate_resource_manager() -> ["Used resource A", "Used resource B"]
    """
    results = []

    async with AsyncResourceManager("Resource_A") as res_a:
        result_a = await res_a.use_resource()
        results.append(result_a)

    async with AsyncResourceManager("Resource_B") as res_b:
        result_b = await res_b.use_resource()
        results.append(result_b)

    return results