"""Google Top Interview Problems & Production Solutions.

Focus areas:
- High-throughput streaming and rate limiting
- Prefix Tree (Trie) backtracking algorithms
- Dynamic / Sliding window constraints
- Stack evaluation and parser mechanics
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional, Set


# ---------------------------------------------------------------------------
# Problem 1: Logger Rate Limiter (LeetCode #359)
# ---------------------------------------------------------------------------

class LoggerRateLimiter:
    """Design a logger system that receives a stream of messages along with their timestamps.

    Each unique message should only be printed at most once every 10 seconds.
    Time Complexity: O(1) per message lookup/insert.
    Space Complexity: O(M) where M is unique message volume.
    """

    def __init__(self) -> None:
        self._msg_history: dict[str, int] = {}

    def should_print_message(self, timestamp: int, message: str) -> bool:
        """Return True if message should be printed in given timestamp, otherwise False."""
        if message in self._msg_history:
            if timestamp - self._msg_history[message] < 10:
                return False
        self._msg_history[message] = timestamp
        return True


# ---------------------------------------------------------------------------
# Problem 2: Fruit Into Baskets / At Most 2 Types (LeetCode #904)
# ---------------------------------------------------------------------------

def total_fruit(fruits: list[int]) -> int:
    """Find the length of the longest contiguous subarray containing at most 2 distinct integers.

    Pattern: Sliding Window with dynamic frequency map.
    Time Complexity: O(N), Space Complexity: O(1) (at most 3 distinct keys).
    """
    count: dict[int, int] = {}
    left = 0
    max_picked = 0

    for right, fruit in enumerate(fruits):
        count[fruit] = count.get(fruit, 0) + 1

        while len(count) > 2:
            left_fruit = fruits[left]
            count[left_fruit] -= 1
            if count[left_fruit] == 0:
                del count[left_fruit]
            left += 1

        max_picked = max(max_picked, right - left + 1)

    return max_picked


# ---------------------------------------------------------------------------
# Problem 3: Word Search II (LeetCode #212)
# ---------------------------------------------------------------------------

class _TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.word: str | None = None


def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """Find all words on a 2D board from a dictionary list using Trie + DFS.

    Time Complexity: O(M * N * 4^(L)) where L is maximum word length.
    Space Complexity: O(W * L) for Trie storage.
    """
    if not board or not board[0] or not words:
        return []

    # Build Trie
    root = _TrieNode()
    for word in words:
        curr = root
        for char in word:
            if char not in curr.children:
                curr.children[char] = _TrieNode()
            curr = curr.children[char]
        curr.word = word

    rows, cols = len(board), len(board[0])
    found_words: list[str] = []

    def _backtrack(r: int, c: int, parent_node: _TrieNode) -> None:
        char = board[r][c]
        if char not in parent_node.children:
            return

        curr_node = parent_node.children[char]
        if curr_node.word is not None:
            found_words.append(curr_node.word)
            curr_node.word = None  # Avoid duplicates

        # Mark cell as visited
        board[r][c] = "#"

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                _backtrack(nr, nc, curr_node)

        # Restore cell
        board[r][c] = char

        # Optimization: prune leaf nodes from Trie
        if not curr_node.children:
            del parent_node.children[char]

    for r in range(rows):
        for c in range(cols):
            _backtrack(r, c, root)

    return found_words


# ---------------------------------------------------------------------------
# Problem 4: Evaluate Reverse Polish Notation (LeetCode #150)
# ---------------------------------------------------------------------------

def eval_rpn(tokens: list[str]) -> int:
    """Evaluate arithmetic expression in Reverse Polish Notation.

    Time Complexity: O(N), Space Complexity: O(N).
    """
    stack: list[int] = []
    ops = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: int(a / b),  # truncate towards zero
    }

    for token in tokens:
        if token in ops:
            b = stack.pop()
            a = stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))

    return stack[0]
