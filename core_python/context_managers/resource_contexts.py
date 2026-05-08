"""Context manager utilities for safe resource handling."""

from __future__ import annotations

import os
from contextlib import AbstractContextManager, contextmanager
from pathlib import Path
from typing import Iterator


@contextmanager
def change_directory(path: Path | str) -> Iterator[Path]:
    """Temporarily change the current working directory."""
    original_path = Path.cwd()
    try:
        os.chdir(Path(path).expanduser().resolve())
        yield Path.cwd()
    finally:
        os.chdir(original_path)


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

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        return False
