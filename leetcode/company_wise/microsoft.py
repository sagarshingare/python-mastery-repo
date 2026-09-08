"""Microsoft Top Interview Problems & Production Solutions.

Focus areas:
- Matrix boundary navigation (Spiral Matrix generation)
- Numerical sign aggregation and overflow prevention
- In-place string word token reversal
- Linked list block-reversal by K groups
"""

from __future__ import annotations

from typing import List, Optional


class ListNode:
    """Singly linked list node."""

    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next


# ---------------------------------------------------------------------------
# Problem 1: Spiral Matrix II (LeetCode #59)
# ---------------------------------------------------------------------------

def generate_matrix(n: int) -> list[list[int]]:
    """Generate an n x n matrix filled with elements from 1 to n^2 in spiral order.

    Time Complexity: O(n^2), Space Complexity: O(n^2).
    """
    matrix = [[0] * n for _ in range(n)]
    left, right = 0, n - 1
    top, bottom = 0, n - 1
    num = 1

    while left <= right and top <= bottom:
        # Traverse right
        for c in range(left, right + 1):
            matrix[top][c] = num
            num += 1
        top += 1

        # Traverse down
        for r in range(top, bottom + 1):
            matrix[r][right] = num
            num += 1
        right -= 1

        # Traverse left
        if top <= bottom:
            for c in range(right, left - 1, -1):
                matrix[bottom][c] = num
                num += 1
            bottom -= 1

        # Traverse up
        if left <= right:
            for r in range(bottom, top - 1, -1):
                matrix[r][left] = num
                num += 1
            left += 1

    return matrix


# ---------------------------------------------------------------------------
# Problem 2: Sign of the Product of an Array (LeetCode #1822)
# ---------------------------------------------------------------------------

def sign_of_product(nums: list[int]) -> int:
    """Return 1 if product is positive, -1 if negative, 0 if zero (avoids overflow).

    Time Complexity: O(N), Space Complexity: O(1).
    """
    negatives = 0
    for num in nums:
        if num == 0:
            return 0
        if num < 0:
            negatives += 1
    return -1 if negatives % 2 != 0 else 1


# ---------------------------------------------------------------------------
# Problem 3: Reverse Words in a String (LeetCode #151)
# ---------------------------------------------------------------------------

def reverse_words(s: str) -> str:
    """Reverse the order of words in a string, stripping excess spaces.

    Time Complexity: O(N), Space Complexity: O(N).
    """
    return " ".join(reversed(s.strip().split()))


# ---------------------------------------------------------------------------
# Problem 4: Reverse Nodes in k-Group (LeetCode #25)
# ---------------------------------------------------------------------------

def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    """Reverse the nodes of a linked list k at a time, leaving remaining nodes untouched.

    Time Complexity: O(N), Space Complexity: O(1).
    """
    # Count total nodes
    count = 0
    curr = head
    while curr:
        count += 1
        curr = curr.next

    dummy = ListNode(0, head)
    prev_group = dummy

    while count >= k:
        curr = prev_group.next
        next_node = curr.next
        for _ in range(k - 1):
            curr.next = next_node.next
            next_node.next = prev_group.next
            prev_group.next = next_node
            next_node = curr.next

        prev_group = curr
        count -= k

    return dummy.next
