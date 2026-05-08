"""Basic file input/output utilities for production Python.

Python version: 3.10+

This module provides safe and reusable utilities for text, JSON, YAML, CSV,
binary, and filesystem operations. Each method includes explicit comments, path
resolution, and directory management to align with production engineering.
"""

from __future__ import annotations

import csv
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

import yaml


def resolve_path(path: Path | str) -> Path:
    """Resolve a filesystem path to an absolute Path object."""
    return Path(path).expanduser().resolve()


def ensure_directory(path: Path | str) -> Path:
    """Ensure that the parent directory exists for a file or directory path."""
    resolved_path = resolve_path(path)
    directory = resolved_path if resolved_path.is_dir() else resolved_path.parent
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def file_exists(path: Path | str) -> bool:
    """Return True if the given file or directory exists."""
    return resolve_path(path).exists()


def list_directory(path: Path | str) -> list[Path]:
    """Return a sorted list of directory entries for the given path."""
    directory = resolve_path(path)
    if not directory.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory}")
    return sorted(directory.iterdir())


def read_text_file(path: Path | str, encoding: str = "utf-8") -> str:
    """Read the entire text content from a file."""
    resolved = resolve_path(path)
    with resolved.open("r", encoding=encoding) as handle:
        return handle.read()


def write_text_file(path: Path | str, content: str, encoding: str = "utf-8") -> None:
    """Write string content to a file and create directories as needed."""
    resolved = resolve_path(path)
    ensure_directory(resolved)
    with resolved.open("w", encoding=encoding) as handle:
        handle.write(content)


def append_text_file(path: Path | str, content: str, encoding: str = "utf-8") -> None:
    """Append string content to a text file."""
    resolved = resolve_path(path)
    ensure_directory(resolved)
    with resolved.open("a", encoding=encoding) as handle:
        handle.write(content)


def safe_write_text_file(path: Path | str, content: str, encoding: str = "utf-8") -> None:
    """Write text content to a temporary file first, then atomically rename it."""
    resolved = resolve_path(path)
    ensure_directory(resolved)
    parent = resolved.parent
    with tempfile.NamedTemporaryFile("w", encoding=encoding, dir=parent, delete=False) as handle:
        handle.write(content)
        temp_file = Path(handle.name)
    temp_file.replace(resolved)


def read_binary_file(path: Path | str) -> bytes:
    """Read raw bytes from a binary file."""
    resolved = resolve_path(path)
    with resolved.open("rb") as handle:
        return handle.read()


def write_binary_file(path: Path | str, data: bytes) -> None:
    """Write raw bytes to a binary file."""
    resolved = resolve_path(path)
    ensure_directory(resolved)
    with resolved.open("wb") as handle:
        handle.write(data)


def read_json_file(path: Path | str, encoding: str = "utf-8") -> Any:
    """Read JSON content from a file and return the parsed object."""
    resolved = resolve_path(path)
    with resolved.open("r", encoding=encoding) as handle:
        return json.load(handle)


def write_json_file(path: Path | str, data: Any, encoding: str = "utf-8") -> None:
    """Write JSON-serializable data to a file with pretty formatting."""
    resolved = resolve_path(path)
    ensure_directory(resolved)
    with resolved.open("w", encoding=encoding) as handle:
        json.dump(data, handle, indent=2)


def read_yaml_file(path: Path | str, encoding: str = "utf-8") -> Any:
    """Read YAML content from a file and return the parsed object."""
    resolved = resolve_path(path)
    with resolved.open("r", encoding=encoding) as handle:
        return yaml.safe_load(handle)


def write_yaml_file(path: Path | str, data: Any, encoding: str = "utf-8") -> None:
    """Write YAML content to a file with readable formatting."""
    resolved = resolve_path(path)
    ensure_directory(resolved)
    with resolved.open("w", encoding=encoding) as handle:
        yaml.safe_dump(data, handle, sort_keys=False)


def read_csv_to_dicts(path: Path | str, encoding: str = "utf-8") -> list[dict[str, str]]:
    """Read CSV rows into a list of dictionaries keyed by column name."""
    resolved = resolve_path(path)
    with resolved.open("r", encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle)
        return [row for row in reader]


def write_dicts_to_csv(path: Path | str, rows: list[dict[str, Any]], fieldnames: list[str] | None = None, encoding: str = "utf-8") -> None:
    """Write a list of dictionaries to a CSV file.

    If fieldnames are not provided, they are inferred from the first row.
    """
    resolved = resolve_path(path)
    ensure_directory(resolved)
    if not rows:
        raise ValueError("rows must contain at least one dictionary")

    fieldnames = fieldnames or list(rows[0].keys())
    with resolved.open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
