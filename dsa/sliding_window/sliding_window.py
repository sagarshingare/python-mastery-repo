"""Sliding window algorithms for subarray/substring problems."""

from __future__ import annotations

from collections import Counter, defaultdict


def max_sum_subarray(nums: list[int], k: int) -> int:
    """Find the maximum sum of a contiguous subarray of size *k*.

    Fixed-size sliding window. O(n).
    """
    if k <= 0 or k > len(nums):
        raise ValueError(f"k={k} is invalid for array of length {len(nums)}")

    window_sum = sum(nums[:k])
    max_sum = window_sum

    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)

    return max_sum


def longest_substring_k_distinct(s: str, k: int) -> str:
    """Return the longest substring with at most *k* distinct characters.

    Variable-size sliding window. O(n).
    """
    if k <= 0:
        return ""

    char_count: dict[str, int] = defaultdict(int)
    start = 0
    best_start = 0
    best_length = 0

    for end, char in enumerate(s):
        char_count[char] += 1

        while len(char_count) > k:
            left_char = s[start]
            char_count[left_char] -= 1
            if char_count[left_char] == 0:
                del char_count[left_char]
            start += 1

        current_length = end - start + 1
        if current_length > best_length:
            best_length = current_length
            best_start = start

    return s[best_start : best_start + best_length]


def min_window_substring(s: str, t: str) -> str:
    """Find the minimum window in *s* that contains all characters of *t*.

    O(n) using two pointers and character counting.
    """
    if not s or not t or len(s) < len(t):
        return ""

    need = Counter(t)
    have: dict[str, int] = defaultdict(int)
    formed = 0
    required = len(need)

    start = 0
    best_start = 0
    best_length = float("inf")

    for end, char in enumerate(s):
        have[char] += 1
        if char in need and have[char] == need[char]:
            formed += 1

        while formed == required:
            window_length = end - start + 1
            if window_length < best_length:
                best_length = window_length
                best_start = start

            left_char = s[start]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                formed -= 1
            start += 1

    return "" if best_length == float("inf") else s[best_start : best_start + int(best_length)]


def max_consecutive_ones(nums: list[int], k: int) -> int:
    """Find the longest subarray of 1s after flipping at most *k* zeros. O(n)."""
    start = 0
    zeros = 0
    max_length = 0

    for end in range(len(nums)):
        if nums[end] == 0:
            zeros += 1

        while zeros > k:
            if nums[start] == 0:
                zeros -= 1
            start += 1

        max_length = max(max_length, end - start + 1)

    return max_length


def count_anagram_substrings(s: str, pattern: str) -> int:
    """Count the number of anagram substrings of *pattern* in *s*. O(n)."""
    if len(pattern) > len(s):
        return 0

    pattern_count = Counter(pattern)
    window_count: Counter[str] = Counter()
    k = len(pattern)
    count = 0

    for i, char in enumerate(s):
        window_count[char] += 1
        if i >= k:
            left_char = s[i - k]
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]
        if window_count == pattern_count:
            count += 1

    return count
