"""Recursion examples: classic problems and patterns."""

from __future__ import annotations

from typing import Any


def factorial(n: int) -> int:
    """Compute n! recursively. O(n).

    Raises:
        ValueError: If *n* is negative.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """Compute the nth Fibonacci number recursively (naive). O(2^n).

    Use the DP module for efficient versions.
    """
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative indices")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def power(base: float, exp: int) -> float:
    """Compute base^exp using fast exponentiation. O(log n)."""
    if exp == 0:
        return 1.0
    if exp < 0:
        return 1.0 / power(base, -exp)
    if exp % 2 == 0:
        half = power(base, exp // 2)
        return half * half
    return base * power(base, exp - 1)


def power_set(items: list[Any]) -> list[list[Any]]:
    """Generate all subsets of *items*. O(2^n).

    Example::

        power_set([1, 2]) → [[], [1], [2], [1, 2]]
    """
    if not items:
        return [[]]
    first = items[0]
    rest_subsets = power_set(items[1:])
    with_first = [[first] + subset for subset in rest_subsets]
    return rest_subsets + with_first


def permutations(items: list[Any]) -> list[list[Any]]:
    """Generate all permutations of *items*. O(n!).

    Example::

        permutations([1, 2]) → [[1, 2], [2, 1]]
    """
    if len(items) <= 1:
        return [items[:]]
    result: list[list[Any]] = []
    for i, item in enumerate(items):
        remaining = items[:i] + items[i + 1 :]
        for perm in permutations(remaining):
            result.append([item] + perm)
    return result


def tower_of_hanoi(n: int, source: str = "A", target: str = "C", auxiliary: str = "B") -> list[tuple[str, str]]:
    """Solve the Tower of Hanoi puzzle and return the list of moves.

    Args:
        n: Number of disks.
        source: Name of the source peg.
        target: Name of the target peg.
        auxiliary: Name of the auxiliary peg.

    Returns:
        List of ``(from_peg, to_peg)`` moves.
    """
    moves: list[tuple[str, str]] = []

    def _solve(disks: int, src: str, tgt: str, aux: str) -> None:
        if disks == 0:
            return
        _solve(disks - 1, src, aux, tgt)
        moves.append((src, tgt))
        _solve(disks - 1, aux, tgt, src)

    _solve(n, source, target, auxiliary)
    return moves


def flood_fill(grid: list[list[int]], row: int, col: int, new_color: int) -> list[list[int]]:
    """Flood-fill a 2-D grid starting from ``(row, col)``.

    Replaces all connected cells of the original color with *new_color*.
    """
    if not grid or not grid[0]:
        return grid

    rows, cols = len(grid), len(grid[0])
    original_color = grid[row][col]

    if original_color == new_color:
        return grid

    def _fill(r: int, c: int) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if grid[r][c] != original_color:
            return
        grid[r][c] = new_color
        _fill(r + 1, c)
        _fill(r - 1, c)
        _fill(r, c + 1)
        _fill(r, c - 1)

    _fill(row, col)
    return grid


def flatten_nested(nested: list[Any]) -> list[Any]:
    """Recursively flatten an arbitrarily nested list."""
    result: list[Any] = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_nested(item))
        else:
            result.append(item)
    return result
