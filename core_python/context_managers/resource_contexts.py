"""
Context manager utilities for safe resource handling, transactions, and dynamic stacks.
========================================================================================
Covers:
- Generator-based context managers (`@contextmanager`)
- Class-based context managers (`__enter__`, `__exit__`)
- Exception suppression vs propagation (`return True` from `__exit__`)
- Transactional commit and rollback semantics
- Dynamic multi-resource management with `contextlib.ExitStack`
- Asynchronous context managers (`@asynccontextmanager`, `__aenter__`, `__aexit__`)
"""

from __future__ import annotations
import asyncio
from contextlib import AbstractContextManager, ExitStack, asynccontextmanager, contextmanager
import logging
import os
from pathlib import Path
import time
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Type

logger = logging.getLogger(__name__)


# --- 1. Generator-based context managers ---

@contextmanager
def change_directory(path: Path | str) -> Iterator[Path]:
    """Temporarily change the current working directory, restoring original on exit."""
    original_path = Path.cwd()
    try:
        target = Path(path).expanduser().resolve()
        os.chdir(target)
        yield target
    finally:
        os.chdir(original_path)


@contextmanager
def execution_timer(label: str = "Block") -> Iterator[dict]:
    """Measure elapsed execution time of a code block."""
    stats = {"start": time.perf_counter(), "elapsed": 0.0}
    try:
        yield stats
    finally:
        stats["elapsed"] = time.perf_counter() - stats["start"]
        logger.info("%s elapsed: %.6fs", label, stats["elapsed"])


# --- 2. Class-based context managers ---

class FileOpenContext(AbstractContextManager[Path]):
    """A custom context manager returning the opened file path after writing."""

    def __init__(self, path: Path | str, content: str) -> None:
        self.path = Path(path).expanduser().resolve()
        self.content = content

    def __enter__(self) -> Path:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            handle.write(self.content)
        return self.path

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        return False


class ManagedTransaction:
    """Demonstrates transactional commit & rollback semantics using __enter__/__exit__.

    If an exception occurs within the block, rollback is executed and the exception propagates.
    If no exception occurs, commit is finalized.
    """

    def __init__(self, target_store: Dict[str, Any]) -> None:
        self.store = target_store
        self._snapshot: Dict[str, Any] = {}
        self.committed: bool = False
        self.rolled_back: bool = False

    def __enter__(self) -> Dict[str, Any]:
        # Capture pre-transaction state
        self._snapshot = self.store.copy()
        return self.store

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Any) -> bool:
        if exc_type is not None:
            # Revert mutations on failure
            self.store.clear()
            self.store.update(self._snapshot)
            self.rolled_back = True
            logger.warning("Transaction rolled back due to %s: %s", exc_type.__name__, exc_val)
            return False  # Propagate exception to caller
        self.committed = True
        logger.info("Transaction committed successfully.")
        return False


class SuppressExceptions(AbstractContextManager[None]):
    """Demonstrates suppressing specific exception types by returning True from __exit__."""

    def __init__(self, *exceptions: Type[BaseException]) -> None:
        self.exceptions = exceptions

    def __enter__(self) -> None:
        pass

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Any) -> bool:
        if exc_type is not None and issubclass(exc_type, self.exceptions):
            logger.info("Suppressed handled exception: %s (%s)", exc_type.__name__, exc_val)
            return True  # Returning True suppresses the exception
        return False


# --- 3. Dynamic Multi-Resource Stacks (ExitStack) ---

def open_multiple_files(paths: List[Path]) -> List[str]:
    """Demonstrates contextlib.ExitStack to dynamically manage a list of open resources."""
    contents: List[str] = []
    with ExitStack() as stack:
        # Dynamically push file handles into the stack; all are guaranteed to close on exit
        handles = [stack.enter_context(p.open("r", encoding="utf-8")) for p in paths]
        for h in handles:
            contents.append(h.read().strip())
    return contents


# --- 4. Asynchronous Context Managers ---

@asynccontextmanager
async def async_resource_connection(resource_name: str) -> AsyncIterator[dict]:
    """Demonstrates asynchronous context manager with setup and teardown."""
    logger.info("Acquiring async resource: %s", resource_name)
    await asyncio.sleep(0.01)
    connection = {"resource": resource_name, "active": True}
    try:
        yield connection
    finally:
        await asyncio.sleep(0.01)
        connection["active"] = False
        logger.info("Released async resource: %s", resource_name)
