"""Utility functions for array-based algorithm practice."""

from __future__ import annotations

from typing import Iterable


def find_two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Find a pair of indices whose values add up to target.

    Args:
        nums: List of integers.
        target: Target sum value.

    Returns:
        A tuple with the two indices, or None when no pair exists.
    """
    index_map: dict[int, int] = {}

    for index, value in enumerate(nums):
        needed = target - value
        if needed in index_map:
            return index_map[needed], index
        index_map[value] = index

    return None


def brute_force_two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Brute force solution with O(n^2) time complexity."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return i, j
    return None
