"""Meta (Facebook) Top Interview Problems & Production Solutions.

Focus areas:
- Two-pointer tolerance checks and string reconstructions
- Stack-based balanced syntax repairs
- Prefix sum and hash table frequencies
- Binary tree column/vertical coordinates and BFS
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, List, Optional


class TreeNode:
    """Node for binary tree traversal."""

    def __init__(self, val: int = 0, left: TreeNode | None = None, right: TreeNode | None = None) -> None:
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------------------
# Problem 1: Valid Palindrome II (LeetCode #680)
# ---------------------------------------------------------------------------

def valid_palindrome_ii(s: str) -> bool:
    """Return True if s can be a palindrome after deleting at most one character.

    Time Complexity: O(N), Space Complexity: O(1).
    """
    def _is_palindrome_range(i: int, j: int) -> bool:
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            # Try skipping either left or right character
            return _is_palindrome_range(left + 1, right) or _is_palindrome_range(left, right - 1)
        left += 1
        right -= 1

    return True


# ---------------------------------------------------------------------------
# Problem 2: Minimum Remove to Make Valid Parentheses (LeetCode #1249)
# ---------------------------------------------------------------------------

def min_remove_to_make_valid(s: str) -> str:
    """Remove minimum number of parentheses '(' or ')' so that the resulting string is valid.

    Time Complexity: O(N), Space Complexity: O(N).
    """
    indices_to_remove: set[int] = set()
    stack: list[int] = []

    for i, char in enumerate(s):
        if char == "(":
            stack.append(i)
        elif char == ")":
            if stack:
                stack.pop()
            else:
                indices_to_remove.add(i)

    # Any unclosed '(' left in the stack must also be removed
    indices_to_remove.update(stack)

    return "".join(char for i, char in enumerate(s) if i not in indices_to_remove)


# ---------------------------------------------------------------------------
# Problem 3: Subarray Sum Equals K (LeetCode #560)
# ---------------------------------------------------------------------------

def subarray_sum(nums: list[int], k: int) -> int:
    """Find the total number of continuous subarrays whose sum equals to k.

    Time Complexity: O(N), Space Complexity: O(N).
    """
    count = 0
    curr_sum = 0
    prefix_map: dict[int, int] = {0: 1}

    for num in nums:
        curr_sum += num
        needed = curr_sum - k
        count += prefix_map.get(needed, 0)
        prefix_map[curr_sum] = prefix_map.get(curr_sum, 0) + 1

    return count


# ---------------------------------------------------------------------------
# Problem 4: Vertical Order Traversal of a Binary Tree (LeetCode #314)
# ---------------------------------------------------------------------------

def vertical_order(root: TreeNode | None) -> list[list[int]]:
    """Return the vertical order traversal of a binary tree's nodes' values from top to bottom, left to right.

    Time Complexity: O(N log N) or O(N) with min/max column tracking.
    Space Complexity: O(N).
    """
    if root is None:
        return []

    column_table: dict[int, list[int]] = defaultdict(list)
    queue: deque[tuple[TreeNode, int]] = deque([(root, 0)])
    min_col = 0
    max_col = 0

    while queue:
        node, col = queue.popleft()
        column_table[col].append(node.val)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

        if node.left is not None:
            queue.append((node.left, col - 1))
        if node.right is not None:
            queue.append((node.right, col + 1))

    return [column_table[col] for col in range(min_col, max_col + 1)]
