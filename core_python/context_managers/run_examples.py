"""Run Python context manager examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging
import tempfile
from pathlib import Path

from core_python.context_managers.resource_contexts import (
    FileOpenContext,
    change_directory,
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

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
        temp_path = Path(temp_file.name)

    try:
        content = "Hello, World!\nThis is a test file."

        with FileOpenContext(temp_path, content) as file_path:
            print(f"File written to: {file_path}")
            with file_path.open('r') as f:
                print(f"File contents: {f.read()}")

        # File should still exist after context manager
        if file_path.exists():
            print("File still exists after context manager")
        else:
            print("File was cleaned up")

    finally:
        if temp_path.exists():
            temp_path.unlink()


def main() -> None:
    """Main entry point for running examples."""
    parser = argparse.ArgumentParser(description="Run Python context manager examples")
    parser.add_argument(
        "--module",
        choices=["change_directory", "file_open"],
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "change_directory":
        run_change_directory_examples()
    elif args.module == "file_open":
        run_file_open_context_examples()
    else:
        # Run all examples
        run_change_directory_examples()
        run_file_open_context_examples()


if __name__ == "__main__":
    main()