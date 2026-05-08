"""LeetCode easy problem: Two Sum."""

from __future__ import annotations

from typing import List


def two_sum_bruteforce(nums: List[int], target: int) -> List[int]:
    """Brute force solution for Two Sum."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    raise ValueError("No two sum solution")


def two_sum_hash(nums: List[int], target: int) -> List[int]:
    """Optimized O(n) Two Sum using a hash table."""
    index_map: dict[int, int] = {}
    for idx, value in enumerate(nums):
        complement = target - value
        if complement in index_map:
            return [index_map[complement], idx]
        index_map[value] = idx
    raise ValueError("No two sum solution")
