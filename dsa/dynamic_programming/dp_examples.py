"""Dynamic programming examples: classic problems with memoisation and tabulation."""

from __future__ import annotations

from functools import lru_cache


def fibonacci_memo(n: int) -> int:
    """Compute the nth Fibonacci number with memoisation. O(n)."""

    @lru_cache(maxsize=None)
    def _fib(k: int) -> int:
        if k <= 1:
            return k
        return _fib(k - 1) + _fib(k - 2)

    return _fib(n)


def fibonacci_tabulation(n: int) -> int:
    """Compute the nth Fibonacci number with tabulation. O(n) time, O(1) space."""
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    """Solve the 0/1 knapsack problem. O(n * capacity).

    Args:
        weights: Weight of each item.
        values: Value of each item.
        capacity: Maximum weight capacity.

    Returns:
        Maximum value achievable.
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])

    return dp[n][capacity]


def longest_common_subsequence(s1: str, s2: str) -> str:
    """Find the longest common subsequence of two strings. O(n * m)."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to build the LCS string
    result: list[str] = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            result.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(reversed(result))


def coin_change(coins: list[int], amount: int) -> int:
    """Find the minimum number of coins to make *amount*. O(n * amount).

    Returns -1 if the amount cannot be made.
    """
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float("inf") else -1  # type: ignore[return-value]


def longest_increasing_subsequence(nums: list[int]) -> int:
    """Find the length of the longest increasing subsequence. O(n log n)."""
    import bisect

    if not nums:
        return 0

    tails: list[int] = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num

    return len(tails)


def edit_distance(word1: str, word2: str) -> int:
    """Compute the Levenshtein edit distance. O(n * m)."""
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]


def max_subarray_sum(nums: list[int]) -> int:
    """Kadane's algorithm for maximum subarray sum. O(n)."""
    if not nums:
        return 0
    max_sum = current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum
