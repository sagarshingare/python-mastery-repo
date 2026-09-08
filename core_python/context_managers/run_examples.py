"""Run Python context manager examples with a simple CLI."""

from __future__ import annotations
import argparse
import asyncio
import logging
from pathlib import Path
import tempfile
from core_python.context_managers.resource_contexts import (
    FileOpenContext,
    ManagedTransaction,
    SuppressExceptions,
    async_resource_connection,
    change_directory,
    execution_timer,
    open_multiple_files,
)

logger = logging.getLogger(__name__)


def run_change_directory_examples() -> None:
    """Demonstrate change_directory context manager."""
    logger.info("Running change_directory examples")

    original_dir = Path.cwd()
    print(f"Original directory: {original_dir}")

    with tempfile.TemporaryDirectory() as temp_dir:
        with change_directory(temp_dir):
            print(f"Inside context: {Path.cwd()}")

    print(f"Back to original: {Path.cwd()}")


def run_file_open_context_examples() -> None:
    """Demonstrate FileOpenContext."""
    logger.info("Running FileOpenContext examples")

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_file:
        temp_path = Path(temp_file.name)

    try:
        content = "Hello, World!\nThis is a test file."
        with FileOpenContext(temp_path, content) as file_path:
            print(f"File written to: {file_path}")
            with file_path.open("r") as f:
                print(f"File contents: {f.read().strip()}")
    finally:
        if temp_path.exists():
            temp_path.unlink()


def run_transaction_and_suppress_examples() -> None:
    """Demonstrate transactional rollback and exception suppression."""
    logger.info("Running transaction and suppression examples")

    # 1. Successful transaction
    account_db = {"Alice": 100, "Bob": 50}
    with ManagedTransaction(account_db) as tx:
        tx["Alice"] -= 20
        tx["Bob"] += 20
    print(f"Committed transaction: {account_db}")
    assert account_db == {"Alice": 80, "Bob": 70}

    # 2. Failed transaction with rollback
    try:
        with ManagedTransaction(account_db) as tx:
            tx["Alice"] -= 50
            raise RuntimeError("Database connection timed out mid-transfer!")
    except RuntimeError as err:
        print(f"Caught transaction failure: {err}")
    print(f"Rolled back state restored: {account_db}")
    assert account_db == {"Alice": 80, "Bob": 70}

    # 3. Exception suppression
    with SuppressExceptions(FileNotFoundError, KeyError):
        missing = account_db["Charlie"]  # Raises KeyError, suppressed!
    print("Execution continued cleanly after suppressed KeyError.")


def run_exitstack_and_async_examples() -> None:
    """Demonstrate ExitStack dynamic resources and async context manager."""
    logger.info("Running ExitStack and async examples")

    # 1. ExitStack with temp files
    with tempfile.TemporaryDirectory() as tmpdir:
        p1 = Path(tmpdir) / "f1.txt"
        p2 = Path(tmpdir) / "f2.txt"
        p1.write_text("file_one_data")
        p2.write_text("file_two_data")

        contents = open_multiple_files([p1, p2])
        print(f"ExitStack dynamically read {len(contents)} files: {contents}")

    # 2. Async context manager
    async def _test_async():
        async with async_resource_connection("RedisCluster") as conn:
            print(f"Async resource active inside context: {conn['active']}")
        print(f"Async resource released outside context: {conn['active']}")

    asyncio.run(_test_async())


def main() -> None:
    """Main entry point for running examples."""
    parser = argparse.ArgumentParser(description="Run Python context manager examples")
    parser.add_argument(
        "--module",
        choices=["change_directory", "file_open", "transaction", "exitstack", "all"],
        default="all",
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "change_directory":
        run_change_directory_examples()
    elif args.module == "file_open":
        run_file_open_context_examples()
    elif args.module == "transaction":
        run_transaction_and_suppress_examples()
    elif args.module == "exitstack":
        run_exitstack_and_async_examples()
    else:
        run_change_directory_examples()
        run_file_open_context_examples()
        run_transaction_and_suppress_examples()
        run_exitstack_and_async_examples()


if __name__ == "__main__":
    main()