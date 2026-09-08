"""Amazon Top Interview Problems & Production Solutions.

Focus areas:
- Custom comparator sorting and stable log reordering
- Multi-source Breadth-First Search (BFS) for propagation/outbreak
- Min/Max Heaps for spatial proximity (K closest points)
- Graph DFS low-link discovery (Tarjan's bridges / critical network links)
"""

from __future__ import annotations

import heapq
from collections import defaultdict, deque
from typing import List


# ---------------------------------------------------------------------------
# Problem 1: Reorder Data in Log Files (LeetCode #937)
# ---------------------------------------------------------------------------

def reorder_log_files(logs: list[str]) -> list[str]:
    """Reorder logs: letter-logs come before digit-logs, sorted lexicographically by content then identifier.

    Digit-logs maintain their original relative order.
    Time Complexity: O(M * N log N) where N is number of logs, M is max log length.
    Space Complexity: O(M * N).
    """
    letter_logs: list[tuple[str, str, str]] = []
    digit_logs: list[str] = []

    for log in logs:
        ident, rest = log.split(" ", 1)
        if rest[0].isdigit():
            digit_logs.append(log)
        else:
            letter_logs.append((rest, ident, log))

    # Sort letter logs primarily by contents, secondarily by identifier
    letter_logs.sort(key=lambda item: (item[0], item[1]))

    return [item[2] for item in letter_logs] + digit_logs


# ---------------------------------------------------------------------------
# Problem 2: Rotting Oranges (LeetCode #994)
# ---------------------------------------------------------------------------

def oranges_rotting(grid: list[list[int]]) -> int:
    """Return the minimum number of minutes until no cell has a fresh orange, or -1 if impossible.

    0 = empty, 1 = fresh, 2 = rotten.
    Pattern: Multi-source BFS.
    Time Complexity: O(R * C), Space Complexity: O(R * C).
    """
    rows, cols = len(grid), len(grid[0])
    queue: deque[tuple[int, int]] = deque()
    fresh_count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh_count += 1

    if fresh_count == 0:
        return 0

    minutes = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue and fresh_count > 0:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh_count -= 1
                    queue.append((nr, nc))

    return minutes if fresh_count == 0 else -1


# ---------------------------------------------------------------------------
# Problem 3: K Closest Points to Origin (LeetCode #973)
# ---------------------------------------------------------------------------

def k_closest_points(points: list[list[int]], k: int) -> list[list[int]]:
    """Return the k closest points to the origin (0, 0) using max-heap.

    Time Complexity: O(N log K), Space Complexity: O(K).
    """
    # Max-heap stores (-dist, x, y)
    max_heap: list[tuple[int, int, int]] = []

    for x, y in points:
        dist_sq = x * x + y * y
        if len(max_heap) < k:
            heapq.heappush(max_heap, (-dist_sq, x, y))
        elif -dist_sq > max_heap[0][0]:
            heapq.heapreplace(max_heap, (-dist_sq, x, y))

    return [[x, y] for _, x, y in max_heap]


# ---------------------------------------------------------------------------
# Problem 4: Critical Connections in a Network (LeetCode #1192)
# ---------------------------------------------------------------------------

def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:
    """Find all critical connections (bridges) in an undirected graph using Tarjan's algorithm.

    Time Complexity: O(V + E), Space Complexity: O(V + E).
    """
    adj: dict[int, list[int]] = defaultdict(list)
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)

    discovery = [-1] * n
    low = [-1] * n
    bridges: list[list[int]] = []
    timer = 0

    def _dfs(u: int, parent: int) -> None:
        nonlocal timer
        discovery[u] = low[u] = timer
        timer += 1

        for v in adj[u]:
            if v == parent:
                continue
            if discovery[v] != -1:
                # Back-edge
                low[u] = min(low[u], discovery[v])
            else:
                _dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > discovery[u]:
                    # (u, v) is a bridge
                    bridges.append([u, v])

    _dfs(0, -1)
    return bridges
