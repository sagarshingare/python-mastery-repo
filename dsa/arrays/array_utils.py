"""
Comprehensive array algorithms and data manipulation utilities.
==============================================================
Covers:
- Two Sum variations (Hash Map & Two Pointers on Sorted Array)
- Two Pointers: Container With Most Water, Remove Duplicates In-Place
- Prefix Sums: O(1) Range Queries, Subarray Sum Equals K
- Kadane's Algorithm: Maximum Subarray Sum (O(n) time, O(1) space)
- Dutch National Flag Algorithm: 3-way in-place partitioning (Sort Colors)
- Intervals: Merge Overlapping Intervals
- Array Rotation: In-place 3-reverse algorithm
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple


# --- 0. Dynamic Array & Search Primitives ---

class DynamicArray:
    """A dynamically resizing array implementation from scratch."""

    def __init__(self, capacity: int = 10) -> None:
        self._capacity = max(1, capacity)
        self._size = 0
        self._data: list[Any] = [None] * self._capacity

    def __len__(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return self._capacity

    def __getitem__(self, index: int) -> Any:
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        return self._data[index]

    def __setitem__(self, index: int, value: Any) -> None:
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        self._data[index] = value

    def append(self, value: Any) -> None:
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = value
        self._size += 1

    def pop(self) -> Any:
        if self._size == 0:
            raise IndexError("pop from empty array")
        value = self._data[self._size - 1]
        self._data[self._size - 1] = None
        self._size -= 1
        if 0 < self._size <= self._capacity // 4:
            self._resize(max(10, self._capacity // 2))
        return value

    def insert(self, index: int, value: Any) -> None:
        if not 0 <= index <= self._size:
            raise IndexError("Index out of range")
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def _resize(self, new_capacity: int) -> None:
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def __repr__(self) -> str:
        return f"DynamicArray({self._data[:self._size]})"


def linear_search(arr: list[Any], target: Any) -> int:
    """Return the index of target in arr using linear search, or -1 if not found. O(n)."""
    for index, val in enumerate(arr):
        if val == target:
            return index
    return -1


def binary_search(arr: list[Any], target: Any) -> int:
    """Return the index of target in a sorted arr using binary search, or -1 if not found. O(log n)."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# --- 1. Two Sum Variations ---

def find_two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Find a pair of indices whose values add up to target using a Hash Map. O(n) time, O(n) space."""
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


def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int] | None:
    """Find two 0-based indices whose values sum to target in an already sorted array.

    Uses two pointers with O(n) time and O(1) auxiliary space.
    """
    left = 0
    right = len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return left, right
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return None


# --- 2. Two Pointers In-Place Operations ---

def container_with_most_water(heights: list[int]) -> int:
    """Compute maximum area of water a container can store. O(n) time, O(1) space."""
    left = 0
    right = len(heights) - 1
    max_area = 0

    while left < right:
        width = right - left
        h = min(heights[left], heights[right])
        max_area = max(max_area, width * h)
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return max_area


def remove_duplicates_inplace(nums: list[int]) -> int:
    """Remove duplicates in-place from a sorted array. Returns the new unique length. O(n) time, O(1) space."""
    if not nums:
        return 0
    write_idx = 1
    for read_idx in range(1, len(nums)):
        if nums[read_idx] != nums[read_idx - 1]:
            nums[write_idx] = nums[read_idx]
            write_idx += 1
    return write_idx


# --- 3. Prefix Sum Utilities ---

class PrefixSum:
    """Computes running prefix sums to answer range sum queries in O(1) time."""

    def __init__(self, nums: list[int]) -> None:
        self.prefix: list[int] = [0] * (len(nums) + 1)
        for i, val in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + val

    def query_range(self, left: int, right: int) -> int:
        """Return sum of elements from index left to right (inclusive). O(1)."""
        if left < 0 or right >= len(self.prefix) - 1 or left > right:
            raise IndexError("Query range out of bounds")
        return self.prefix[right + 1] - self.prefix[left]

    query = query_range


def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    """Count total number of continuous subarrays whose sum equals k. O(n) time, O(n) space."""
    prefix_counts: dict[int, int] = {0: 1}
    current_sum = 0
    count = 0

    for num in nums:
        current_sum += num
        needed = current_sum - k
        count += prefix_counts.get(needed, 0)
        prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1

    return count


# --- 4. Kadane's Algorithm: Maximum Subarray Sum ---

def max_subarray_sum(nums: list[int]) -> int:
    """Find the contiguous subarray with the largest sum using Kadane's algorithm. O(n) time, O(1) space."""
    if not nums:
        raise ValueError("nums must be non-empty")
    current_max = nums[0]
    global_max = nums[0]

    for x in nums[1:]:
        current_max = max(x, current_max + x)
        global_max = max(global_max, current_max)

    return global_max


# --- 5. Dutch National Flag (3-way partition) ---

def sort_colors(nums: list[int]) -> None:
    """Sort an array containing 0s, 1s, and 2s in-place in a single pass. O(n) time, O(1) space."""
    low = 0
    mid = 0
    high = len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1


# --- 6. Intervals ---

def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merge all overlapping intervals. O(n log n) time, O(n) space."""
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged: list[list[int]] = [sorted_intervals[0]]

    for current in sorted_intervals[1:]:
        prev = merged[-1]
        if current[0] <= prev[1]:
            # Overlapping intervals: extend end bound
            prev[1] = max(prev[1], current[1])
        else:
            merged.append(current)

    return merged


# --- 7. Array Rotation ---

def rotate_array_inplace(nums: list[int], k: int) -> None:
    """Rotate array to the right by k steps in-place using the 3-reversals algorithm. O(n) time, O(1) space."""
    if not nums:
        return
    n = len(nums)
    k = k % n
    if k == 0:
        return

    def reverse_slice(start: int, end: int) -> None:
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1

    # 1. Reverse entire array
    reverse_slice(0, n - 1)
    # 2. Reverse first k elements
    reverse_slice(0, k - 1)
    # 3. Reverse remaining n - k elements
    reverse_slice(k, n - 1)
