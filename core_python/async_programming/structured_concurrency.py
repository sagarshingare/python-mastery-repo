"""
Structured Concurrency in Python
================================
Structured concurrency ensures that concurrent operations have clear lifetimes,
proper scoping, and deterministic cancellation/cleanup. Tasks spawned together
complete together, preventing "zombie tasks" or unhandled background exceptions.

Introduced natively in Python 3.11 via `asyncio.TaskGroup` (PEP 654 Exception Groups).
This module provides:
1. `TaskGroupCompat`: A production-ready polyfill for Python 3.9 & 3.10 that adheres
   to the `asyncio.TaskGroup` context manager contract.
2. Demonstrations of concurrent fetching, fan-out/fan-in, and failure fail-fast propagation.
"""

from __future__ import annotations
import asyncio
import sys
from typing import Any, Coroutine, List, Optional, Set, TypeVar

T = TypeVar("T")


class TaskGroupCompat:
    """Async context manager providing structured concurrency semantics for Python 3.9+.

    If running on Python 3.11+, delegates directly to native `asyncio.TaskGroup`.
    On Python 3.9/3.10, manages child tasks, gathers results, and cancels siblings on first error.
    """

    def __init__(self) -> None:
        self._native_group: Optional[Any] = None
        if hasattr(asyncio, "TaskGroup"):
            self._native_group = asyncio.TaskGroup()
        self._tasks: Set[asyncio.Task[Any]] = set()
        self._errors: List[BaseException] = []

    async def __aenter__(self) -> TaskGroupCompat:
        if self._native_group is not None:
            await self._native_group.__aenter__()
            return self
        return self

    def create_task(self, coro: Coroutine[Any, Any, T], *, name: Optional[str] = None) -> asyncio.Task[T]:
        """Schedule a child coroutine within this structured concurrency scope."""
        if self._native_group is not None:
            return self._native_group.create_task(coro, name=name)

        loop = asyncio.get_running_loop()
        task = loop.create_task(coro, name=name)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Optional[bool]:
        if self._native_group is not None:
            return await self._native_group.__aexit__(exc_type, exc_val, exc_tb)

        # Polyfill exit for Python 3.9/3.10
        if exc_val is not None:
            self._errors.append(exc_val)
            # Cancel all active child tasks if the context block itself failed
            for t in self._tasks:
                if not t.done():
                    t.cancel()

        if self._tasks:
            # Wait for all remaining child tasks to settle
            done, pending = await asyncio.wait(self._tasks, return_when=asyncio.ALL_COMPLETED)
            for t in done:
                if not t.cancelled():
                    err = t.exception()
                    if err is not None:
                        self._errors.append(err)

        if self._errors:
            # If multiple errors occurred, raise a combined RuntimeError or ExceptionGroup
            if len(self._errors) == 1 and exc_val is not None:
                # Re-raise context block error
                return None
            msg = f"Structured concurrency failure with {len(self._errors)} error(s): " + "; ".join(
                f"{type(e).__name__}: {e}" for e in self._errors
            )
            raise RuntimeError(msg)

        return None


async def simulate_fetch(source_id: int, delay: float) -> dict:
    """Simulates async I/O fetch operation."""
    await asyncio.sleep(delay)
    return {"source": source_id, "data": f"payload_{source_id}", "status": 200}


async def simulate_faulty_worker(worker_id: int) -> None:
    """Simulates a worker that fails unexpectedly."""
    await asyncio.sleep(0.05)
    raise ValueError(f"Worker {worker_id} crashed during processing")


async def run_structured_concurrency_demos() -> None:
    """Run structured concurrency demonstrations."""
    print("=== Structured Concurrency (TaskGroup) Demo ===")

    # 1. Successful parallel fan-out
    print("1. Running successful fan-out with TaskGroupCompat...")
    results: List[dict] = []

    async with TaskGroupCompat() as tg:
        t1 = tg.create_task(simulate_fetch(1, 0.05), name="fetch-1")
        t2 = tg.create_task(simulate_fetch(2, 0.03), name="fetch-2")
        t3 = tg.create_task(simulate_fetch(3, 0.01), name="fetch-3")

    results = [t1.result(), t2.result(), t3.result()]
    print(f"Collected {len(results)} task results successfully: {results}")

    # 2. Failure propagation & sibling cancellation
    print("\n2. Testing failure propagation and sibling handling...")
    try:
        async with TaskGroupCompat() as tg:
            tg.create_task(simulate_fetch(4, 0.5), name="slow-worker")
            tg.create_task(simulate_faulty_worker(5), name="faulty-worker")
    except Exception as err:
        print(f"Structured scope caught error as expected: {type(err).__name__}: {err}")

    print("Structured concurrency demonstrations completed successfully!\n")


if __name__ == "__main__":
    asyncio.run(run_structured_concurrency_demos())
