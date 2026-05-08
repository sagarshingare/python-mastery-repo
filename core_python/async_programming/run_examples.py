"""Run async programming examples with a simple CLI."""

from __future__ import annotations

import argparse
import asyncio
import logging
from pathlib import Path

from core_python.async_programming.async_basics import (
    async_calculate_sum,
    async_delayed_greeting,
    async_fetch_data,
    run_concurrent_operations,
    run_sequential_operations,
)
from core_python.async_programming.async_concurrency import (
    concurrent_data_processing,
    demonstrate_resource_manager,
    producer_consumer_pattern,
    semaphore_limited_concurrency,
)
from core_python.async_programming.async_tasks import (
    cancel_running_tasks,
    create_and_run_tasks,
    handle_task_exceptions,
    run_with_timeout,
)
from core_python.async_programming.event_loops import (
    create_task_and_monitor,
    demonstrate_executor_usage,
    demonstrate_loop_manager,
    run_async_from_sync,
    run_async_in_thread,
)


async def run_async_basics_examples() -> None:
    """Run basic async programming examples."""
    print("\n=== Async Basics Examples ===")

    print("async_delayed_greeting('World', 0.1):")
    result = await async_delayed_greeting("World", 0.1)
    print(f"Result: {result}")

    print("\nasync_calculate_sum([1, 2, 3, 4, 5]):")
    result = await async_calculate_sum([1, 2, 3, 4, 5])
    print(f"Result: {result}")

    print("\nasync_fetch_data('database'):")
    result = await async_fetch_data("database")
    print(f"Result: {result}")

    print("\nrun_sequential_operations():")
    results = await run_sequential_operations()
    print(f"Results: {results}")

    print("\nrun_concurrent_operations():")
    results = await run_concurrent_operations()
    print(f"Results: {results}")


async def run_async_tasks_examples() -> None:
    """Run async task management examples."""
    print("\n=== Async Tasks Examples ===")

    print("create_and_run_tasks():")
    results = await create_and_run_tasks()
    print(f"Results: {results}")

    print("\nrun_with_timeout():")
    results = await run_with_timeout()
    print(f"Results: {results}")

    print("\nhandle_task_exceptions():")
    results = await handle_task_exceptions()
    print(f"Results: {results}")

    print("\ncancel_running_tasks():")
    result = await cancel_running_tasks()
    print(f"Result: {result}")


async def run_async_concurrency_examples() -> None:
    """Run concurrent execution examples."""
    print("\n=== Async Concurrency Examples ===")

    print("producer_consumer_pattern():")
    result = await producer_consumer_pattern()
    print(f"Result: {result}")

    print("\nsemaphore_limited_concurrency():")
    results = await semaphore_limited_concurrency()
    print(f"Results: {results}")

    test_data = [
        {"id": 1, "value": 10},
        {"id": 2, "value": 20},
        {"id": 3, "value": 30}
    ]
    print(f"\nconcurrent_data_processing({test_data}):")
    results = await concurrent_data_processing(test_data)
    print(f"Results: {results}")

    print("\ndemonstrate_resource_manager():")
    results = await demonstrate_resource_manager()
    print(f"Results: {results}")


async def run_event_loops_examples() -> None:
    """Run event loop management examples."""
    print("\n=== Event Loops Examples ===")

    print("demonstrate_executor_usage():")
    result = await demonstrate_executor_usage()
    print(f"Result: {result}")

    print("\ncreate_task_and_monitor():")
    result = await create_task_and_monitor()
    print(f"Result: {result}")

    print("\ndemonstrate_loop_manager():")
    result = await demonstrate_loop_manager()
    print(f"Result: {result}")


def run_sync_examples() -> None:
    """Run synchronous examples that use async internally."""
    print("\n=== Synchronous Integration Examples ===")

    print("run_async_in_thread():")
    result = run_async_in_thread()
    print(f"Result: {result}")

    print("\nrun_async_from_sync():")
    result = run_async_from_sync()
    print(f"Result: {result}")


async def run_all_async_examples() -> None:
    """Run all async programming examples."""
    await run_async_basics_examples()
    await run_async_tasks_examples()
    await run_async_concurrency_examples()
    await run_event_loops_examples()
    run_sync_examples()


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Run async programming examples.")
    parser.add_argument(
        "--module",
        choices=["basics", "tasks", "concurrency", "loops", "sync", "all"],
        default="all",
        help="Module to run"
    )
    args = parser.parse_args()

    if args.module == "basics":
        asyncio.run(run_async_basics_examples())
    elif args.module == "tasks":
        asyncio.run(run_async_tasks_examples())
    elif args.module == "concurrency":
        asyncio.run(run_async_concurrency_examples())
    elif args.module == "loops":
        asyncio.run(run_event_loops_examples())
    elif args.module == "sync":
        run_sync_examples()
    else:
        asyncio.run(run_all_async_examples())


if __name__ == "__main__":
    main()